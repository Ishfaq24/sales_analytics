import pandas as pd

def load_csv_data(paths: dict):
    return {
        name: pd.read_csv(path)
        for name, path in paths.items()
    }
