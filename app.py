# Pharmacy Management System - Streamlit Frontend

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from fpdf import FPDF
import base64

def load_inventory():
    return pd.DataFrame({
        "Item": ["Paracetamol", "Ibuprofen", "Amoxicillin"],
        "Quantity": [100, 50, 200],
        "Price": [1.5, 2.0, 0.8]
    })

@st.cache_data
def get_cached_inventory():
    return load_inventory()

def generate_report_from_inventory(inventory):
    total_items = inventory["Quantity"].sum()
    total_value = (inventory["Quantity"] * inventory["Price"]).sum()
    top_product = inventory.loc[inventory["Quantity"].idxmax(), "Item"]

    return pd.DataFrame({
        "Report Section": ["Total Inventory Value", "Total Items", "Top Product"],
        "Details": [f"${total_value:.2f}", f"{total_items} items", top_product]
    })

def create_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Pharmacy Management System Report", ln=True, align='C')

    for i, row in dataframe.iterrows():
        pdf.cell(200, 10, txt=f"{row['Report Section']}: {row['Details']}", ln=True)

    return pdf

def download_pdf(pdf):
    pdf_output = pdf.output(dest="S").encode("latin1", errors="ignore")
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="report.pdf">Download Report as PDF</a>'
    return href

def main():
    st.set_page_config(page_title="Pharmacy Management System", layout="wide")

    if "inventory" not in st.session_state:
        st.session_state.inventory = get_cached_inventory().copy()

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
            "Main Menu", ["🏠 Home", "📦 Inventory", "➕ Add Product", "📊 Sales", "📈 Reports"],
            icons=["house", "box", "plus-circle", "graph-up", "bar-chart"],
            menu_icon="cast", default_index=0
        )

    if selected == "🏠 Home":
        st.title("🏥 Pharmacy Management System")
        st.write("Welcome to the **Pharmacy Management System**! Manage your inventory, track sales, and generate reports effortlessly.")

    elif selected == "📦 Inventory":
        st.title("📦 Inventory Management")

        # Display inventory with delete buttons
        for index, row in st.session_state.inventory.iterrows():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
            col1.write(row['Item'])
            col2.write(row['Quantity'])
            col3.write(row['Price'])
            delete_button = col5.button("Delete", key=f"delete_{index}")

            if delete_button:
                st.session_state.inventory = st.session_state.inventory.drop(index).reset_index(drop=True)
                st.experimental_rerun()

        st.dataframe(st.session_state.inventory, width='stretch')

    elif selected == "➕ Add Product":
        st.title("➕ Add New Product")

        with st.form("add_item_form"):
            st.subheader("Add New Item")
            new_item = st.text_input("Item Name")
            new_quantity = st.number_input("Quantity", min_value=0, step=1)
            new_price = st.number_input("Price", min_value=0.0, step=0.1)
            submitted = st.form_submit_button("Add Item")

            if submitted:
                new_row = {"Item": new_item, "Quantity": new_quantity, "Price": new_price}
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Item '{new_item}' added successfully!")

    elif selected == "📊 Sales":
        st.title("📊 Sales Tracking")
        sales = load_inventory()  # Placeholder for sales data
        st.dataframe(sales, width='stretch')

    elif selected == "📈 Reports":
        st.title("📈 Reports")
        report_data = generate_report_from_inventory(st.session_state.inventory)
        st.dataframe(report_data, width='stretch')

        pdf = create_pdf(report_data)
        href = download_pdf(pdf)
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()