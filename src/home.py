import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
from streamlit import components

from sklearn.feature_extraction.text import TfidfVectorizer
from similarity import spdt
from similarity.ngrams import ngrams
from product import Product

# Function to create a custom HTML for the scorecard
def create_scorecard(title, value, hex_color):
    html = f"""
    <div style="
        background-color: {hex_color};
        border-radius: 10px;
        padding: 10px 20px;
        text-align: center;
        color: white;
        margin: 10px;
        ">
        <h4 style="margin:0;">{title}</h4>
        <h1 style="margin:0;">{value}</h1>
    </div>
    """
    return html

st.set_page_config(layout="wide")

# Load the data (update the path to where the data is located on your machine)
catalog = pd.read_pickle('data/processed/catalog.pkl')

# Clean the data
catalog[['Brand', 'Type']] = catalog[['Brand', 'Type']].fillna('Others')

# Calculate metrics for the scorecard
total_products = catalog.shape[0]
total_brands = catalog['Brand'].nunique()
total_types = catalog['Type'].nunique()

# Sidebar navigation
st.sidebar.header('Navigation')
page = st.sidebar.radio("Go to", ('Dashboard Catalog', 'Product Catalog App'))

# Display content based on the state
if page == 'Dashboard Catalog':
    st.title(':clipboard: Dashboard Catalog')

    # Scorecards with custom styling
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(create_scorecard("Total Products", total_products, "#1abc9c"), unsafe_allow_html=True)
    with col2:
        st.markdown(create_scorecard("Total Brands", total_brands, "#3498db"), unsafe_allow_html=True)
    with col3:
        st.markdown(create_scorecard("Total Types", total_types, "#9b59b6"), unsafe_allow_html=True)

    st.markdown("---")  # Divider
    # Bar chart for Brand with labels
    st.subheader("Number of Products by Brand")
    brand_counts = catalog['Brand'].value_counts().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.barh(brand_counts.index, brand_counts.values)
    ax.bar_label(bars)
    st.pyplot(fig)

    st.markdown("---")  # Divider
    # Bar chart for Type with labels
    st.subheader("Number of Products by Type")
    type_counts = catalog['Type'].value_counts().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.barh(type_counts.index, type_counts.values)
    ax.bar_label(bars)
    st.pyplot(fig)

elif page == 'Product Catalog App':
    
    # Title
    st.title(''':books: Product Catalog App''')
    st.markdown('---')

    # Sub
    st.subheader('Optimize operations by navigating POS variability')
    st.write(
        '''
        In today's digital world, managing data efficiently is crucial, 
        and a key part of this is having a good data catalog. 
        A data catalog helps organize information, 
        making it easy to access and use. 
        However, when data comes from different places, 
        like product names from various Point of Sale (POS) systems, 
        inconsistencies arise and it may lead to bad reporting 
        and decision-making.
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