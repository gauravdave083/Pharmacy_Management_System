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
        "Price": [1.5, 2.0, 0.8],
        "Product Type": ["💊", "💊", "💊"]
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
        # Remove unsupported characters
        section = row['Report Section'].encode('latin1', 'ignore').decode('latin1')
        details = row['Details'].encode('latin1', 'ignore').decode('latin1')
        pdf.cell(200, 10, txt=f"{section}: {details}", ln=True)

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

    # Ensure inventory table and add product attributes are consistent
    if "Type" not in st.session_state.inventory.columns:
        def assign_product_type(item_name):
            if item_name.lower() in ["paracetamol", "ibuprofen", "amoxicillin"]:
                return "Tablet 💊"
            elif "syrup" in item_name.lower():
                return "Syrup 🥤"
            elif "injection" in item_name.lower():
                return "Injection 💉"
            else:
                return "Other 🛒"

        st.session_state.inventory["Type"] = st.session_state.inventory["Item"].apply(assign_product_type)

    # Update product names to include dynamic emojis in front
    st.session_state.inventory["Item"] = st.session_state.inventory.apply(
        lambda row: f"{row['Type']} {row['Item']}", axis=1
    )

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
        st.title("🏥 Welcome to the Pharmacy Management System")
        st.image("https://via.placeholder.com/800x300.png?text=Pharmacy+Management+System", use_container_width=True)
        st.write("""
        Welcome to the **Pharmacy Management System**! This platform helps you:
        - Manage your inventory efficiently.
        - Track sales and generate insightful reports.
        - Add new products and keep your stock updated.
        - Download detailed reports in PDF format.
        
        ### Features:
        - 📦 **Inventory Management**: Keep track of all your products.
        - ➕ **Add Products**: Add new items to your inventory.
        - 📊 **Sales Tracking**: Monitor your sales performance.
        - 📈 **Reports**: Generate and download reports effortlessly.
        
        ### Get Started:
        Use the sidebar to navigate through the system and explore its features.
        """)

        st.info("Tip: Check out the Reports tab to see a summary of your inventory!")
        st.success("New Feature: You can now add products dynamically and see them reflected in the reports!")

    elif selected == "📦 Inventory":
        st.title("📦 Inventory Management")
        st.dataframe(st.session_state.inventory, width='stretch')

    elif selected == "➕ Add Product":
        st.title("➕ Add New Product")

        with st.form("add_item_form"):
            st.subheader("Add New Item")
            new_item = st.text_input("Item Name")
            new_quantity = st.number_input("Quantity", min_value=0, step=1)
            new_price = st.number_input("Price", min_value=0.0, step=0.1)
            product_type = st.selectbox("Product Type", ["Tablet 💊", "Syrup 🥤", "Injection 💉", "Other 🛒"])
            submitted = st.form_submit_button("Add Item")

            if submitted:
                # Sanitize the input to remove unsupported characters
                sanitized_item = new_item.encode('latin1', 'ignore').decode('latin1')
                new_row = {"Item": sanitized_item, "Quantity": new_quantity, "Price": new_price, "Type": product_type}
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Item '{sanitized_item}' added successfully!")

    elif selected == "📊 Sales":
        st.title("📊 Sales Tracking")
        sales = load_inventory()  # Placeholder for sales data
        st.dataframe(sales, width='stretch')

    elif selected == "📈 Reports":
        st.title("📈 Reports")
        # Dynamically generate the report based on the current inventory
        report_data = generate_report_from_inventory(st.session_state.inventory)
        st.dataframe(report_data, width='stretch')

        pdf = create_pdf(report_data)
        href = download_pdf(pdf)
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()