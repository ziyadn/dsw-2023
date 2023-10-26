import os
import pandas as pd

import utils
import product

def preprocessing(data: pd.DataFrame):
    # 1. Drop null values
    data = data.dropna(subset=['Product Name'])

    # 2. Extract clean name, formula, and metrics
    data['Name'] = data['Product Name'].apply(lambda name: product.Product(name).name)
    data['Formula'] = data['Product Name'].apply(lambda name: product.Product(name).formula)
    data['Metrics'] = data['Product Name'].apply(lambda name: product.Product(name).metrics)

    return data