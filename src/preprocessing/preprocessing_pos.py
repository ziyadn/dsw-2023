import pandas as pd

def preprocessing(data: pd.DataFrame):
    # 1. Drop null values
    data = data.dropna(subset=['Product Name'])

    # 2. Drop duplicates
    data = data.drop_duplicates().reset_index(drop=True)

    # 3. Extract clean name, formula, and metrics
    data['Name'] = data['Product Name'].apply(lambda product: product.name)
    data['Formula'] = data['Product Name'].apply(lambda product: product.formula)
    data['Metrics'] = data['Product Name'].apply(lambda product: product.metrics)
    data['Product Name'] = data['Product Name'].apply(lambda product: product.full_name)

    return data