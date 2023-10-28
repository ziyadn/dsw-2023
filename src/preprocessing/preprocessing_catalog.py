import pandas as pd

def preprocessing(data: pd.DataFrame) -> pd.DataFrame:
    data = data.drop_duplicates(subset=['Product SKU']).reset_index(drop=True)

    return data