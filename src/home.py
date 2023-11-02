import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from similarity import spdt
from similarity.ngrams import ngrams
from product import Product

# Load data catalog
catalog = pd.read_pickle('data\processed\catalog.pkl')

# Title
st.title(':potted_plant: Product Catalog App')

# Header
st.header(':books: Harmonize data catalog')

# Sub
st.subheader('Optimize operations by navigating POS variability')
st.write(
    '''
    In today's digital world, managing data efficiently is crucial, and a key part of this is having a good data catalog. A data catalog helps organize information, making it easy to access and use. However, when data comes from different places, like product names from various Point of Sale (POS) systems, inconsistencies arise and it may lead to bad reporting and decision-making.
    '''
)

st.subheader(':mag: Search product')
st.write(
    '''
    Input your product name in search box below. Then we will suggest similar items from current catalog.
    '''
)

# Search box for item name
search_term = st.text_input('Search by Item Name', '')
catalog_name = catalog['Product SKU']

# Calculate similarity
data = pd.concat(
    [
        pd.Series([search_term]),
        catalog_name
    ],
    ignore_index=True
)

vectorizer = TfidfVectorizer(min_df=2, analyzer=ngrams)
tf_idf_matrix = vectorizer.fit_transform(data)

matches = spdt.awesome_cossim_top(
    tf_idf_matrix,
    tf_idf_matrix.transpose(),
    ntop=100,
    lower_bound=0.5
)

matches_df = spdt.get_matches_df(
    matches, 
    data, 
    top=200
)

matches_df = matches_df[matches_df['similarity'] < 0.9999]
similar_item = matches_df[matches_df['left_side'] == search_term]['right_side'].unique()

# Show search result
st.write('Suggestion based on your input:')
st.dataframe(
        data=catalog[catalog['Product SKU'].isin(similar_item)],
        use_container_width=True
)

# Create new item
st.write('Cannot find your item?')
if st.button('Create new item'):
    new_product = Product(search_term)
    st.header(':new: Add new item')

    # Input fields for new item
    new_name = st.text_input('Product SKU', new_product.name)
    new_brand = st.text_input('Brand', '')
    new_type = st.text_input('Type', '')
    new_formula = st.text_input('Formula', new_product.formula)
    new_metrics = st.text_input('Metrics', new_product.metrics)

    if st.button('Submit'):
        # Add new item to the DataFrame
        new_row = {
            'Product SKU': new_name,
            'Brand': new_brand,
            'Type': new_type,
            'Formula': new_formula,
            'Metrics': new_metrics
        }
        new_row = pd.DataFrame(data=new_row, index=[0])
        data = pd.concat([data, new_row], ignore_index=True)
        st.write('New item added successfully!')