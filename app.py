# Pharmacy Management System - Streamlit Frontend with MongoDB Backend

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from fpdf import FPDF
import base64
from datetime import datetime
import uuid

# Import API client
from api_client import get_api_client, check_api_connection, handle_api_error

@st.cache_data(ttl=60)  # Cache for 1 minute
def load_inventory():
    """Load inventory from API"""
    api_client = get_api_client()
    result = api_client.get_medications(page_size=100)  # Get all medications
    
    if result and 'data' in result:
        return api_client.medications_to_dataframe(result)
    else:
        # Fallback to empty dataframe if API fails
        return pd.DataFrame(columns=['Item', 'Quantity', 'Price', 'Type'])

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_cached_inventory():
    """Get cached inventory data"""
    return load_inventory()

def generate_report_from_inventory(inventory):
    """Generate report data from inventory DataFrame"""
    if inventory.empty:
        return pd.DataFrame({
            "Report Section": ["Total Inventory Value", "Total Items", "Top Product"],
            "Details": ["$0.00", "0 items", "No products"]
        })
    
    total_items = inventory["Quantity"].sum()
    total_value = (inventory["Quantity"] * inventory["Price"]).sum()
    
    if not inventory.empty:
        top_product = inventory.loc[inventory["Quantity"].idxmax(), "Item"]
    else:
        top_product = "No products"

    return pd.DataFrame({
        "Report Section": ["Total Inventory Value", "Total Items", "Top Product"],
        "Details": [f"${total_value:.2f}", f"{total_items} items", top_product]
    })

def create_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(200, 10, text="Pharmacy Management System Report", new_x="LMARGIN", new_y="NEXT", align='C')

    for i, row in dataframe.iterrows():
        # Remove unsupported characters
        section = str(row['Report Section']).encode('latin1', 'ignore').decode('latin1')
        details = str(row['Details']).encode('latin1', 'ignore').decode('latin1')
        pdf.cell(200, 10, text=f"{section}: {details}", new_x="LMARGIN", new_y="NEXT")

    return pdf

def download_pdf(pdf):
    # Get the PDF output as bytes
    pdf_output = pdf.output()
    # Encode to base64 for download
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="report.pdf">Download Report as PDF</a>'
    return href

def main():
    st.set_page_config(page_title="Pharmacy Management System", layout="wide")
    
    # Check API connection first
    if not check_api_connection():
        st.stop()
    
    # Initialize API client
    api_client = get_api_client()

    if "inventory" not in st.session_state:
        st.session_state.inventory = get_cached_inventory().copy()

    # Refresh inventory data periodically
    if st.button("� Refresh Data"):
        st.cache_data.clear()
        st.session_state.inventory = get_cached_inventory().copy()
        st.success("Data refreshed successfully!")
        st.rerun()

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
        st.image("https://via.placeholder.com/800x300.png?text=Pharmacy+Management+System", width="stretch")
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
        
        # Show current inventory
        inventory_data = get_cached_inventory()
        if not inventory_data.empty:
            st.dataframe(inventory_data, width='stretch')
            
            # Show additional inventory metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                total_items = inventory_data["Quantity"].sum()
                st.metric("Total Items", f"{total_items:,}")
            with col2:
                total_value = (inventory_data["Quantity"] * inventory_data["Price"]).sum()
                st.metric("Total Value", f"${total_value:,.2f}")
            with col3:
                low_stock_count = len(inventory_data[inventory_data["Quantity"] < 50])
                st.metric("Low Stock Items", low_stock_count)
        else:
            st.warning("No inventory data available. Please check the API connection.")

    elif selected == "➕ Add Product":
        st.title("➕ Add New Product")

        with st.form("add_item_form"):
            st.subheader("Add New Medication")
            
            # Basic Information
            col1, col2 = st.columns(2)
            with col1:
                new_item = st.text_input("Medication Name*", help="Enter the medication name")
                generic_name = st.text_input("Generic Name", help="Generic/scientific name")
                category = st.selectbox("Category", 
                    ["Analgesic", "Antibiotic", "NSAID", "Antidiabetic", "Cough Suppressant", "Other"])
            
            with col2:
                manufacturer = st.text_input("Manufacturer", help="Pharmaceutical company")
                dosage_form = st.selectbox("Dosage Form", 
                    ["Tablet", "Capsule", "Syrup", "Injection", "Cream", "Other"])
                strength = st.text_input("Strength", help="e.g., 500mg, 100IU/ml")
            
            # Pricing and Stock
            col3, col4 = st.columns(2)
            with col3:
                new_price = st.number_input("Unit Price ($)*", min_value=0.0, step=0.01, format="%.2f")
                new_quantity = st.number_input("Initial Stock Quantity*", min_value=0, step=1)
            
            with col4:
                reorder_level = st.number_input("Reorder Level", min_value=0, step=1, value=10)
                prescription_required = st.checkbox("Prescription Required")
            
            # Additional Information
            barcode = st.text_input("Barcode", help="Optional: Product barcode")
            batch_number = st.text_input("Batch Number", help="Manufacturing batch number")
            
            submitted = st.form_submit_button("Add Medication")

            if submitted:
                if not new_item or new_price <= 0 or new_quantity < 0:
                    st.error("Please fill in all required fields with valid values.")
                else:
                    # Prepare medication data for API
                    medication_data = {
                        "name": new_item.strip(),
                        "generic_name": generic_name.strip() if generic_name else None,
                        "category": category,
                        "manufacturer": manufacturer.strip() if manufacturer else None,
                        "dosage_form": dosage_form,
                        "strength": strength.strip() if strength else None,
                        "unit_price": float(new_price),
                        "quantity_in_stock": int(new_quantity),
                        "reorder_level": int(reorder_level),
                        "prescription_required": prescription_required
                    }
                    
                    # Add optional fields
                    if barcode.strip():
                        medication_data["barcode"] = barcode.strip()
                    if batch_number.strip():
                        medication_data["batch_number"] = batch_number.strip()
                    
                    # Create medication via API
                    try:
                        result = api_client.create_medication(medication_data)
                        if result:
                            st.success(f"✅ Medication '{new_item}' added successfully!")
                            # Clear cache to refresh data
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("❌ Failed to add medication. Please check the form and try again.")
                    except Exception as e:
                        st.error(f"❌ Error adding medication: {str(e)}")

    elif selected == "📊 Sales":
        st.title("📊 Sales Tracking")
        
        # Get sales data from API
        sales_result = api_client.get_sales(page_size=50)
        
        if sales_result and 'data' in sales_result and sales_result['data']:
            sales_data = sales_result['data']
            
            # Convert to DataFrame for display
            sales_df = pd.DataFrame(sales_data)
            
            # Format columns for better display
            display_columns = ['invoice_number', 'sale_date', 'total_amount', 'payment_method', 'payment_status']
            available_columns = [col for col in display_columns if col in sales_df.columns]
            
            if available_columns:
                sales_display = sales_df[available_columns].copy()
                
                # Rename columns
                column_mapping = {
                    'invoice_number': 'Invoice',
                    'sale_date': 'Date',
                    'total_amount': 'Total ($)',
                    'payment_method': 'Payment Method',
                    'payment_status': 'Status'
                }
                sales_display = sales_display.rename(columns=column_mapping)
                
                # Format date and total
                if 'Date' in sales_display.columns:
                    sales_display['Date'] = pd.to_datetime(sales_display['Date']).dt.strftime('%Y-%m-%d %H:%M')
                if 'Total ($)' in sales_display.columns:
                    sales_display['Total ($)'] = sales_display['Total ($)'].astype(float).round(2)
                
                st.dataframe(sales_display, width='stretch')
                
                # Sales metrics
                total_sales = sum(float(sale.get('total_amount', 0)) for sale in sales_data)
                avg_sale = total_sales / len(sales_data) if sales_data else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Sales", f"${total_sales:,.2f}")
                with col2:
                    st.metric("Number of Transactions", len(sales_data))
                with col3:
                    st.metric("Average Sale", f"${avg_sale:.2f}")
            else:
                st.dataframe(sales_df, width='stretch')
        else:
            st.info("No sales data available yet.")

    elif selected == "📈 Reports":
        st.title("📈 Reports")
        
        # Generate report from current inventory
        inventory_data = get_cached_inventory()
        report_data = generate_report_from_inventory(inventory_data)
        
        st.subheader("📊 Inventory Summary Report")
        st.dataframe(report_data, width='stretch')
        
        # Additional reports
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔔 Low Stock Alerts")
            if not inventory_data.empty:
                low_stock = inventory_data[inventory_data["Quantity"] < 50]
                if not low_stock.empty:
                    st.dataframe(low_stock[['Item', 'Quantity', 'Type']], width='stretch')
                else:
                    st.success("✅ All items are well stocked!")
            else:
                st.info("No inventory data to analyze.")
        
        with col2:
            st.subheader("💰 Sales Summary")
            # Get daily sales report
            daily_sales = api_client.get_daily_sales_report()
            if daily_sales:
                st.metric("Today's Sales", f"${daily_sales.get('total_sales', 0):,.2f}")
                st.metric("Transactions Today", daily_sales.get('total_transactions', 0))
                st.metric("Average Sale", f"${daily_sales.get('average_sale', 0):.2f}")
            else:
                st.info("No sales data available for today.")

        # PDF Download
        st.subheader("📥 Download Report")
        pdf = create_pdf(report_data)
        href = download_pdf(pdf)
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()