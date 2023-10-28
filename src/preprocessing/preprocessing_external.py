import pandas as pd

def preprocessing(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    data = data.drop_duplicates().reset_index(drop=True)

    data['Formula'] = data['Nama Produk'].apply(lambda name: name.get_formula())

    for key, values in config['external_data_keywords'].items():
        data['Type'] = data['Nama Produk'].apply(lambda name: values if key in name.full_name.lower() else 'Others')
    data['Type'] = data.apply(lambda row: 'Majemuk' if  not(pd.isnull(row['Formula'])) and row['Type'] == 'Others' else row['Type'], axis=1)
    
    data['Nama Produk'] = data['Nama Produk'].apply(lambda name: name.full_name)
    data = data.rename(columns={'Nama Produk': 'Product SKU'})

    return data