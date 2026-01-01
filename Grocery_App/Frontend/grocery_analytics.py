import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

API_URL = "http://localhost:8000"

def grocery_analytics():
    st.subheader("Grocery Analytics")
    col1, col2 = st.columns(2)
    with col1:
        month = st.selectbox("Month", ["All"] + list(range(1, 13)),key = "Analytics_month")
    with col2:
        year = st.selectbox("Year", list(range(2025, 2031)),key = "Analytics Year")
    response = requests.get(f"{API_URL}/groceries/{month}/{year}")
    groceries = response.json()

    total_items = len(groceries)
    bought_items = len([1 for g in groceries if g["is_bought"] == 1])
    pending_items  = total_items-bought_items
    bought_pct = round((bought_items/total_items)*100,2)
    unique_products = set(g['grocery_item'] for g in groceries)
    all_products = list(g['grocery_item'] for g in groceries)
    unique_products_count = len(unique_products)
    unique_places = len(set(g['place_bought'] for g in groceries))
    # item_counts = {
    #     item:all_products.count(item) for item in unique_products
    # }
    col1,col2,col3,col4,col5,col6 = st.columns([2,2,2,2,2,2])

    with col1:
        st.metric("Total Items ",total_items)
    with col2:
        st.metric("Total bought Items ",bought_items)
    with col3:
        st.metric("Total Pending Items ",pending_items)
    with col4:
        st.metric("Bought percentage ",bought_pct)
    with col5:
        st.metric("Total unique products ",unique_products_count)
    with col6:
        st.metric("Total unique place ", unique_places)

    st.divider()

    # Top 5 frequently added items
    st.subheader("Top 5 frequently bought items")
    data_df  = pd.DataFrame(groceries)

    item_counts = (
        data_df["grocery_item"].str.strip().str.lower().value_counts().head(5)
    )
    st.bar_chart(item_counts)

    st.divider()

    # Place wise breakdown
    st.subheader("Place wise breakdown")

    place_counts = (
        data_df['place_bought'].str.strip().str.lower().value_counts()
    )

    st.bar_chart(place_counts)

    st.divider()

    st.subheader("Number of items per month")

    # Number of items per month
    data_df["date_column"] = pd.to_datetime(data_df['date_value'],format = '%Y-%m-%d')
    actual_data = (
        data_df
        .groupby(data_df["date_column"].dt.month)
        .size()
        .reset_index(name="count")
    )

    st.bar_chart(
        actual_data.set_index("date_column")['count']
    )
