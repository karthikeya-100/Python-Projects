import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

# Used to check if a row is updated
def is_row_dirty(row):
    fields = ["grocery_item","quantity_value","quantity_unit","place_bought"]
    return any(row[f] != row["original"][f] for f in fields)


def add_update_groceries():


    # Initializing session
    if "groceries" not in st.session_state:
        st.session_state.groceries =[]
    if "key" not in st.session_state:
        st.session_state.key = None
    if "delete_message" not in st.session_state:
        st.session_state.delete_message = None
    if "add_message" not in st.session_state:
        st.session_state.add_message = None
    if "update_message" not in st.session_state:
        st.session_state.update_message = None

    col1 , col2 = st.columns(2)
    with col1:
       month =  st.selectbox("Month",options = list(range(1,13)))
    with col2:
       year =  st.selectbox("Year",options = list(range(2025,2031)))
    current_key = f"{month}-{year}"

    # Displaying of messages after each operation
    if st.session_state.delete_message:
        st.toast(st.session_state.delete_message)
        st.session_state.delete_message = None
    if st.session_state.add_message:
        st.toast(st.session_state.add_message)
        st.session_state.add_message = None
    if st.session_state.update_message:
        st.toast(st.session_state.update_message)
        st.session_state.update_message = None

    #Loading rows for first time and whenever date changes
    if st.session_state.key != current_key:
        response = requests.get(f"{API_URL}/groceries/{month}/{year}")
        data = response.json()
        st.session_state.groceries = [
            {
                "grocery_id": g["grocery_id"],
                "grocery_item": g["grocery_item"],
                "quantity_value": g["quantity_value"],
                "quantity_unit": g["quantity_unit"],
                "place_bought": g["place_bought"],
                "is_bought": g["is_bought"],
                "is_new": False,
                "is_dirty": False, # to track if a row is updated or not
                "original" :g.copy()
            }
            for g in data
        ]
        st.session_state.key = current_key


    # rendering rows
    for index,grocery in enumerate(st.session_state.groceries):
        row_key = grocery['grocery_id'] or f"new{index}" # Unique id so that there will be no bugs when rows are deleted
        col1, col2, col3, col4, col5, col6 = st.columns([3,2,2,2,1,1])
        with col1:
            grocery["grocery_item"] = st.text_input(label = "Item",value = grocery["grocery_item"],key = f"item_{row_key}")
        with col2:
            grocery["quantity_value"] = st.number_input(label = "Value" ,min_value=0.0,value = grocery[
                "quantity_value"],key = f"value_{row_key}")
        with col3:
            grocery["quantity_unit"] = st.text_input(label = "Unit" ,value = grocery["quantity_unit"],key = f"unit_"
                                                                                                            f"{row_key}")
        with col4:
            grocery["place_bought"] = st.text_input(label = "Place_bought" ,value = grocery["place_bought"] ,
                                                    key = f"place_{row_key}")
        grocery["is_dirty"] = is_row_dirty(grocery)
        with col5:
            new_value_bought = st.checkbox(label = "Bought" ,value = bool(grocery["is_bought"]),key = f"bought{row_key}")
            new_value_int = int(new_value_bought)
            if grocery["is_bought"] != new_value_int:
                requests.patch(f"{API_URL}/groceries/{new_value_int}/{grocery["grocery_id"]}")
                grocery["is_bought"] = new_value_int
        with col6:
            delete_button = st.button("Delete",key = f"delete_{row_key}")
            if delete_button:
                if grocery["grocery_id"]:
                    requests.delete(f"{API_URL}/groceries/{grocery["grocery_id"]}")
                st.session_state.groceries.pop(index)
                st.session_state.delete_message = "Grocery Deleted Successfully"
                st.rerun()

    add_col,save_col = st.columns([0.5,0.5])
    with add_col:
        add_button = st.button("Add")
        if add_button:
            st.session_state.groceries.append({
                "grocery_id": "",
                "grocery_item": "",
                "quantity_value": 0.0,
                "quantity_unit": "",
                "place_bought": "",
                "is_bought": 0,
                "is_new": True,
                "is_dirty": True,
                "original" :{
                    "grocery_id" : "",
                    "grocery_item" : "",
                    "quantity_value" : 0.0,
                    "quantity_unit" : "",
                    "place_bought" : "",
                    "is_bought" : 0
                }
            })
            st.rerun()
    print(st.session_state.groceries)
    with save_col:
        save_button = st.button('Save')
        if save_button:
            for grocery in st.session_state.groceries:

                if grocery["is_new"]:

                    payload = {
                        "grocery_item" : grocery["grocery_item"],
                        "quantity_value" : grocery["quantity_value"],
                        "quantity_unit" : grocery["quantity_unit"],
                        "place_bought" : grocery["place_bought"]
                    }
                    response = requests.post(f"{API_URL}/groceries/{month}/{year}",json = payload)
                    data = response.json()
                    grocery["grocery_id"] = data["grocery_id"]
                    grocery["is_new"] = False
                    st.session_state.add_message = "Groceries added successfully"


                elif grocery["is_dirty"]:
                    payload = {
                        "grocery_item" : grocery["grocery_item"],
                        "quantity_value" : grocery["quantity_value"],
                        "quantity_unit" : grocery["quantity_unit"],
                        "place_bought" : grocery["place_bought"]
                    }
                    requests.patch(f"{API_URL}/groceries/{grocery["grocery_id"]}/{month}/{year}",json=payload)
                    st.session_state.update_message = "Grocery Updated successfully"

                grocery["is_dirty"] = False
                grocery["original"] = {
                    "grocery_item": grocery["grocery_item"],
                    "quantity_value": grocery["quantity_value"],
                    "quantity_unit": grocery["quantity_unit"],
                    "place_bought": grocery["place_bought"],
                    "is_bought": grocery["is_bought"]
                }
            st.rerun()

