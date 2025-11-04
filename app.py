# Pharmacy Management System - Streamlit Frontend

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

def load_inventory():
    return pd.DataFrame({
        "Item": ["💊 Paracetamol", "💊 Ibuprofen", "💊 Amoxicillin"],
        "Quantity": [100, 50, 200],
        "Price": [1.5, 2.0, 0.8]
    })

def load_sales():
    return pd.DataFrame({
        "Date": ["2025-11-01", "2025-11-02"],
        "Item": ["💊 Paracetamol", "💊 Ibuprofen"],
        "Quantity": [10, 5],
        "Total": [15.0, 10.0]
    })

def main():
    st.set_page_config(page_title="Pharmacy Management System", layout="wide")

    with st.sidebar:
        st.markdown("""
        <style>
        .css-1v3fvcr .option-menu div {
            font-size: 18px !important;
            font-weight: bold !important;
            color: #4CAF50 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        selected = option_menu(
            "Main Menu", ["🏠 Home", "📦 Inventory", "📊 Sales", "📈 Reports"],
            icons=["house", "box", "graph-up", "bar-chart"],
            menu_icon="cast", default_index=0
        )

    if selected == "🏠 Home":
        st.title("🏥 Pharmacy Management System")
        st.write("Welcome to the **Pharmacy Management System**! Manage your inventory, track sales, and generate reports effortlessly.")
    elif selected == "📦 Inventory":
        st.title("📦 Inventory Management")
        inventory = load_inventory()
        st.dataframe(inventory, use_container_width=True)
    elif selected == "📊 Sales":
        st.title("📊 Sales Tracking")
        sales = load_sales()
        st.dataframe(sales, use_container_width=True)
    elif selected == "📈 Reports":
        st.title("📈 Reports")
        st.write("Generate and view detailed reports here.")

if __name__ == "__main__":
    main()