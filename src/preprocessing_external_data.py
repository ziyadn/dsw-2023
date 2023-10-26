import os
import pandas as pd

import utils
import product

def get_formula(data: pd.DataFrame) -> pd.DataFrame:
    data['Formula'] = data['Nama Produk'].apply(lambda name: product.Product(name).get_formula())

    return data

def get_product_type(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    for key, values in config['external_data_keywords'].items():
        data['Type'] = data['Nama Produk'].apply(lambda name: values if key in name.lower() else 'Others')

    data['Type'] = data.apply(lambda row: 'Majemuk' if  not(pd.isnull(row['Formula'])) and row['Type'] == 'Others' else row['Type'], axis=1)

    return data

if __name__ == '__main__':
    # 1. Load config file
    file_dir = os.path.dirname(__file__)
    config = utils.load_config()

    # 2. Load data
    data = pd.read_csv(
        os.path.join(file_dir, config['external_data_path'])
    )
    data = data.drop_duplicates()
    data = data.reset_index(drop=True)

    # 3. Get formula
    data = get_formula(data)

    # 4. Get product type
    data = get_product_type(data, config)

    # 5. Dump data
    data.to_csv(
        os.path.join(file_dir, config['external_data_processed_path']), 
        index=False
    )