import streamlit as st
import requests


API_URL = "http://localhost:8000"

# API calls
def fetch_groceries(month,year):
    response = requests.get(f"{API_URL}/groceries/{month}/{year}")
    data = response.json()
    return data

def insert_grocery(month,year,grocery_item,quantity_value,quantity_unit,place_bought):
    print(type(month),type(year),grocery_item,quantity_value,quantity_unit,place_bought)
    payload = {
        "grocery_item" : grocery_item,
        "quantity_value" : quantity_value,
        "quantity_unit" : quantity_unit,
        "place_bought" : place_bought
    }
    requests.post(f"{API_URL}/groceries/{month}/{year}",json=payload)

def is_row_dirty(row):
        fields = ["grocery_item","quantity_value","quantity_unit","place_bought"]
        print(f"Current_row{row}")
        return any(row[f] != row["original"][f] for f in fields)

def manage_groceries():

    # Initializing session
    if "groceries" not in st.session_state:
        st.session_state.groceries = []
    if "key" not in st.session_state:
        st.session_state.key = None

    col1 , col2 = st.columns(2)
    with col1:
        month = st.selectbox("Month",list(range(1,13)))
    with col2:
        year = st.selectbox("Year",list(range(2025,2031)))
    current_key = f"{month}-{year}"

    if st.session_state.key != current_key:
        data = fetch_groceries(month,year)
        st.session_state.groceries = [
            {
                "grocery_id":g["grocery_id"],
                "grocery_item": g["grocery_item"],
                "quantity_value":g["quantity_value"],
                "quantity_unit" : g["quantity_unit"],
                "place_bought" :g["place_bought"],
                # Dirty Tracking for is bought button
                "is_bought" : g["is_bought"],
                "prev_is_bought" : g["is_bought"],

                #dirty tracking for row updates
                "original" : {
                    "grocery_item" : g["grocery_item"],
                    "quantity_value" : str(g["quantity_value"]),
                    "quantity_unit" : g["quantity_unit"],
                    "place_bought" : g["place_bought"],
                    "is_bought" : g["is_bought"]
                },
                "is_new": False,
                "is_dirty":False
             }
            for g in data
        ]
        st.session_state.key = current_key
        print(st.session_state.key)

    #rendering groceries
    st.subheader("Groceries")

    for idx,grocery in enumerate(st.session_state.groceries):
        col1,col2,col3,col4,col5,col6,col7 = st.columns([3,2,2,2,1,1,1])

        with col1:
            grocery["grocery_item"] = st.text_input("Item",value=grocery["grocery_item"],key=f"item_{idx}")
        with col2:
            grocery["quantity_value"] = st.text_input("Quantity",value=grocery["quantity_value"],key=f"value"
                                                                                                          f"_{idx}")
        with col3:
            grocery["quantity_unit"] = st.text_input("Unit",value = grocery["quantity_unit"],key=f"unit_{idx}")
        with col4:
            grocery["place_bought"] = st.text_input("Place Bought",value=grocery["place_bought"],key=f"place_{idx}")
        with col5:
            new_value = st.checkbox("Bought",value = bool(grocery["is_bought"]) ,key= f"bought_{idx}")
            new_value_int = int(new_value)
            if grocery["grocery_id"] and new_value_int != grocery["prev_is_bought"]:
                requests.patch(f"{API_URL}/groceries/{new_value_int}/{grocery["grocery_id"]}")
                grocery["prev_is_bought"] = new_value_int
                grocery["is_bought"] = new_value_int
        with col6:
            if st.button("Delete",key = f"delete_{idx}"):
                if grocery["grocery_id"]:
                    requests.delete(f"{API_URL}/groceries/{grocery["grocery_id"]}")
                st.session_state.groceries.pop(idx)
                st.rerun()
        grocery["is_dirty"] = is_row_dirty(grocery)
        # with col7:
        #     is_disabled = not(grocery["is_new"] or grocery["is_dirty"])
        #     print(is_disabled)
        #     if st.button("Update",key=f"update_{idx}",disabled=is_disabled):
        #         if grocery["is_new"]:
        #             payload = {
        #                 "grocery_item" :grocery["grocery_item"],
        #                 "quantity_value" : grocery["quantity_value"],
        #                 "quantity_unit" : grocery["quantity_unit"],
        #                 "place_bought" : grocery["place_bought"]
        #             }
        #             response = requests.post(f"{API_URL}/groceries/{month}/{year}",json=payload).json()
        #             grocery["grocery_id"] = response["grocery_id"]
        #             print("hit")
        #             grocery["is_new"] = False
        #             grocery["is_dirty"] = False
        #
        #             grocery["original"] = payload | {"is_bought" : grocery["is_bought"]}
        #         elif grocery["is_dirty"]:
        #             payload = {
        #                 "grocery_item" : grocery["grocery_item"],
        #                 "quantity_value" : grocery["quantity_value"],
        #                 "quantity_unit" : grocery["quantity_unit"],
        #                 "place_bought" : grocery["place_bought"]
        #             }
        #             requests.patch(f"{API_URL}/groceries/{grocery["grocery_id"]}",json=payload)
        #             grocery["is_dirty"] = False
        #             grocery['original'] = payload | {"is_bought" : grocery["is_bought"]}

    add_col,save_col = st.columns(2)
    with add_col:
        add_button = st.button("Add")
        if add_button:
            st.session_state.groceries.append({
                "grocery_id":"",
                "grocery_item":"",
                "quantity_value":"",
                "quantity_unit":"",
                "place_bought":"",
                "is_bought":0,
                "prev_is_bought" :0,
                "is_new":True,
                "is_dirty":True,
                "original" :{
                    "grocery_item":"",
                    "quantity_value":"",
                    "quantity_unit":"",
                    "place_bought":"",
                    "is_bought":0
                }
            })
            st.rerun()


    with save_col:
        save_button = st.button("Save")
        if save_button:
            for g in st.session_state.groceries:

                # INSERT
                if g["is_new"]:
                    response = requests.post(
                        f"{API_URL}/groceries/{month}/{year}",
                        json={
                            "grocery_item": g["grocery_item"],
                            "quantity_value": g["quantity_value"],
                            "quantity_unit": g["quantity_unit"],
                            "place_bought": g["place_bought"]
                        }
                    ).json()

                    g["grocery_id"] = response["grocery_id"]
                    g["is_new"] = False

                # UPDATE
                elif g["is_dirty"]:
                    requests.patch(
                        f"{API_URL}/groceries/{g['grocery_id']}/{month}/{year}",
                        json={
                            "grocery_item": g["grocery_item"],
                            "quantity_value": g["quantity_value"],
                            "quantity_unit": g["quantity_unit"],
                            "place_bought": g["place_bought"]
                        }
                    )

                # RESET SNAPSHOT (for both cases)
                g["is_dirty"] = False
                g["original"] = {
                    "grocery_item": g["grocery_item"],
                    "quantity_value": g["quantity_value"],
                    "quantity_unit": g["quantity_unit"],
                    "place_bought": g["place_bought"],
                    "is_bought": g["is_bought"]
                }

            st.success("Saved successfully ✅")
            st.rerun()

