import streamlit as st
from manage_groceries import manage_groceries
from add_update_groceries import add_update_groceries
from grocery_analytics import grocery_analytics


st.set_page_config(page_title="Grocery App", layout="wide")
st.title("🛒 Grocery Tracker")

st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
html, body, [class*="css"]  {
    font-size: 15px;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ---------- INPUTS ---------- */
input, textarea {
    border-radius: 10px !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background-color: #1f2933 !important;
    border-radius: 10px;
}

/* ---------- GROCERY ROW ---------- */
.grocery-card {
    padding: 12px 10px;
    border-radius: 14px;
    background: linear-gradient(180deg, #111827, #0b1220);
    margin-bottom: 12px;
    border: 1px solid #1f2937;
}

/* ---------- CHECKBOX ALIGN ---------- */
.stCheckbox {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: 28px;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-weight: 600;
    height: 42px;
}

/* Delete button */
button[key^="delete"] {
    background-color: #7f1d1d !important;
    color: white !important;
}
button[key^="delete"]:hover {
    background-color: #991b1b !important;
}

/* Add button */
button:has-text("Add") {
    background-color: #065f46 !important;
    color: white !important;
}
button:has-text("Add"):hover {
    background-color: #047857 !important;
}

/* Save button */
button:has-text("Save") {
    background-color: #1d4ed8 !important;
    color: white !important;
}
button:has-text("Save"):hover {
    background-color: #2563eb !important;
}

/* ---------- MOBILE ---------- */
@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .grocery-card {
        padding: 14px;
    }

    .stCheckbox {
        padding-top: 10px;
    }

    .stButton > button {
        height: 44px;
        font-size: 15px;
    }
}

</style>
""", unsafe_allow_html=True)




(tab1,tab2) = st.tabs(["Manage Groceries","Analytics"])

with tab1:
   add_update_groceries()
with tab2:
    grocery_analytics()
