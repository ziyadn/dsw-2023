import pandas as pd
import utils

from product import Product
from preprocessing import preprocessing_catalog, preprocessing_pos, preprocessing_external

def main():
    config = utils.load_config()

    catalog = pd.read_excel(
        config['catalog_data_path'],
        sheet_name=config['catalog_data_sheet']
    )
    catalog = preprocessing_catalog.preprocessing(catalog)

    pos = pd.read_excel(
        config['pos_data_path'],
        sheet_name=config['pos_data_sheet']
    )
    pos = pos.dropna()
    pos['Product Name'] = pos['Product Name'].apply(lambda name: Product(name))
    pos = preprocessing_pos.preprocessing(pos)
    pos = pos.rename(columns={'Product Name': 'Full Name'})
    pos['Product SKU'] = pos.apply(lambda row: row['Name'] if pd.isnull(row['Formula']) else f'{row["Name"]}{row["Formula"]}', axis=1)
    pos = pos.drop(columns=['Name'], axis=1)
    pos['Brand'] = None
    pos['Type'] = None
    pos = pos[['Product SKU', 'Brand', 'Type', 'Formula', 'Metrics', 'Full Name']]

    external = pd.read_csv(
        config['external_data_path'],
        delimiter=';'
    )
    external['Nama Produk'] = external['Nama Produk'].apply(lambda name: Product(name))
    external = preprocessing_external.preprocessing(external, config)
    external = external[['Product SKU', 'Brand', 'Type', 'Formula']]

    catalog_external = pd.concat(
        [
            catalog,
            external
        ], ignore_index=True
    )
    catalog_external = catalog_external.reset_index(drop=True)

    catalog.to_pickle(config['catalog_data_processed_path'])
    pos.to_pickle(config['pos_data_processed_path'])
    external.to_pickle(config['external_data_processed_path'])
    catalog_external.to_pickle(config['catalog_external_processed_path'])

if __name__ == '__main__':
    main()