import streamlit as st
import pandas as pd

# Sample DataFrame (Replace this with your own dataset)
data = {
    'Item Name': ['Apple', 'Banana', 'Orange', 'Strawberry', 'Blueberry'],
    'Category': ['Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit'],
    'Color': ['Red', 'Yellow', 'Orange', 'Red', 'Blue']
}

df = pd.DataFrame(data)

# App Name and Description
st.title("Item Search and Filter App")
st.write("This app allows you to search for items and apply filters.")

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Search & Filter", "Add New Item"])

if page == "Search & Filter":
    # Search Box for Item Name
    search_term = st.text_input("Search by Item Name", "")

    # Drop-down filters based on DataFrame
    category_filter = st.selectbox('Filter by Category', df['Category'].unique())
    color_filter = st.selectbox('Filter by Color', df['Color'].unique())

    # Filtering the DataFrame based on user inputs
    filtered_df = df[
        (df['Item Name'].str.contains(search_term, case=False)) &
        (df['Category'] == category_filter) &
        (df['Color'] == color_filter)
    ]

    # Display the filtered DataFrame
    st.write("Filtered Data:")
    st.write(filtered_df)

elif page == "Add New Item":
    st.header("Add a New Item")

    # Input fields for new item information
    new_name = st.text_input("Item Name")
    new_category = st.text_input("Category")
    new_color = st.text_input("Color")

    if st.button("Submit"):
        # Add new item to the DataFrame
        new_row = {'Item Name': new_name, 'Category': new_category, 'Color': new_color}
        new_row = pd.DataFrame(data=new_row, index=[0])
        df = pd.concat([df, new_row], ignore_index=True)
        st.write("New item added successfully!")

# Display the DataFrame
st.write("Current DataFrame:")
st.write(df)
