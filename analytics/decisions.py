import numpy as np

def safe_number(value, default=0.0):
    """
    Convert NaN / inf / invalid values to a safe float.
    Production-safe: handles any input type.
    """
    try:
        value = float(value)
        if np.isnan(value) or np.isinf(value):
            return default
        return value
    except (TypeError, ValueError):
        return default


def executive_decision_engine(df, monthly_sales, growth_rate):
    decisions = {}

    # ------------------------------------------------
    # Ensure revenue exists
    # ------------------------------------------------
    if "revenue" not in df.columns:
        df = df.copy()
        df["revenue"] = df["quantity"] * df["price"]

    # ------------------------------------------------
    # BUSINESS HEALTH SCORE (DEFENSIVE)
    # ------------------------------------------------
    avg_growth = safe_number(growth_rate.dropna().mean())
    growth_score = min(max(avg_growth * 5, 0), 40)

    mean_sales = safe_number(monthly_sales.mean(), default=1.0)
    std_sales = safe_number(monthly_sales.std())

    revenue_consistency = safe_number(
        100 - (std_sales / mean_sales) * 100
    )
    consistency_score = min(max(revenue_consistency * 0.4, 0), 30)

    total_revenue = safe_number(df["revenue"].sum(), default=1.0)
    top_category_revenue = safe_number(
        df.groupby("category")["revenue"].sum().max()
    )

    concentration_ratio = safe_number(
        top_category_revenue / total_revenue
    )

    diversification_score = 30 if concentration_ratio < 0.6 else 10

    raw_health_score = (
        growth_score + consistency_score + diversification_score
    )

    decisions["health_score"] = int(
        min(max(safe_number(raw_health_score), 0), 100)
    )

    # ------------------------------------------------
    # RISK DETECTION (STABLE)
    # ------------------------------------------------
    risks = []

    if avg_growth < 0:
        risks.append(
            "Revenue growth is negative. Immediate action required."
        )

    if concentration_ratio > 0.65:
        risks.append(
            "Revenue is highly concentrated in a single category."
        )

    recent_drop = safe_number(
        monthly_sales.pct_change().dropna().min()
    )

    if recent_drop < -0.25:
        risks.append(
            "Sharp revenue drop detected in recent months."
        )

    decisions["risks"] = risks

    # ------------------------------------------------
    # STRATEGIC RECOMMENDATIONS (SAFE)
    # ------------------------------------------------
    recommendations = []

    if not df.empty and "region" in df.columns:
        region_revenue = (
            df.groupby("region")["revenue"].sum()
        )

        if not region_revenue.empty:
            top_region = region_revenue.idxmax()
            weak_region = region_revenue.idxmin()

            recommendations.append(
                f"Invest more in {top_region} region where revenue is strongest."
            )
            recommendations.append(
                f"Improve performance in {weak_region} region via targeted initiatives."
            )

    if concentration_ratio > 0.65:
        recommendations.append(
            "Diversify into secondary product categories to reduce dependency risk."
        )

    decisions["recommendations"] = recommendations

    return decisions
