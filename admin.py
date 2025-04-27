import streamlit as st
import pandas as pd
from database import Database

# Initialize the database
db = Database()

# Set page configuration
st.set_page_config(
    page_title="Inventory Admin",
    page_icon="🔧",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'admin_page' not in st.session_state:
    st.session_state.admin_page = "login"
if 'edit_item_id' not in st.session_state:
    st.session_state.edit_item_id = None

# Simple admin authentication (in a real app, use more secure methods)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"  # In a real app, use hashed passwords and environment variables

# Function to handle admin login
def admin_login(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.session_state.admin_logged_in = True
        st.session_state.admin_page = "dashboard"
        st.experimental_rerun()
    else:
        st.error("Invalid username or password")

# Function to handle admin logout
def admin_logout():
    st.session_state.admin_logged_in = False
    st.session_state.admin_page = "login"
    st.experimental_rerun()

# Function to navigate between admin pages
def admin_navigate_to(page):
    st.session_state.admin_page = page
    st.experimental_rerun()

# Function to set item for editing
def set_edit_item(item_id):
    st.session_state.edit_item_id = item_id
    admin_navigate_to("edit_item")

# Admin Login Page
def show_admin_login():
    st.title("Inventory Admin")
    st.subheader("Login")

    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            admin_login(username, password)

# Admin Dashboard
def show_admin_dashboard():
    st.title("Inventory Admin Dashboard")

    # Create a sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        st.button("Add New Item", on_click=admin_navigate_to, args=("add_item",))
        st.button("View Borrowing History", on_click=admin_navigate_to, args=("borrowing_history",))
        st.button("Logout", on_click=admin_logout)

    st.header("Current Inventory")

    # Get all items from the database
    items = db.get_all_items()

    if not items:
        st.info("No items in the inventory.")
    else:
        # Convert to DataFrame for better display
        df = pd.DataFrame(items, columns=["ID", "Code", "Name", "Category", "Location", "Description", "Available"])

        # Replace boolean values with more readable text
        df["Available"] = df["Available"].map({1: "Yes", 0: "No"})

        # Add action buttons
        st.dataframe(df)

        st.subheader("Item Actions")
        col1, col2 = st.columns(2)

        with col1:
            item_id = st.number_input("Enter Item ID to Edit", min_value=1, step=1)
            st.button("Edit Item", on_click=set_edit_item, args=(item_id,))

        with col2:
            delete_id = st.number_input("Enter Item ID to Delete", min_value=1, step=1)
            if st.button("Delete Item"):
                success, message = db.delete_item(delete_id)
                if success:
                    st.success(message)
                    st.experimental_rerun()
                else:
                    st.error(message)

# Add Item Page
def show_add_item():
    st.title("Add New Item")

    # Create a sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        st.button("Back to Dashboard", on_click=admin_navigate_to, args=("dashboard",))
        st.button("Logout", on_click=admin_logout)

    with st.form("add_item_form"):
        code = st.text_input("Item Code (must be unique)")
        name = st.text_input("Item Name")
        category = st.text_input("Category")
        location = st.text_input("Storage Location")
        description = st.text_area("Description")

        submit_button = st.form_submit_button("Add Item")

        if submit_button:
            if not code or not name:
                st.error("Code and Name are required fields")
            else:
                success = db.add_item(code, name, category, location, description)
                if success:
                    st.success(f"Item '{name}' added successfully!")
                    # Clear form fields by navigating back to the same page
                    admin_navigate_to("add_item")
                else:
                    st.error("Failed to add item. Code might already exist.")

# Edit Item Page
def show_edit_item():
    st.title("Edit Item")

    # Create a sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        st.button("Back to Dashboard", on_click=admin_navigate_to, args=("dashboard",))
        st.button("Logout", on_click=admin_logout)

    item_id = st.session_state.edit_item_id

    # Get the item details
    item = db.get_item_by_id(item_id)

    if not item:
        st.error(f"Item with ID {item_id} not found")
        st.button("Back to Dashboard", on_click=admin_navigate_to, args=("dashboard",))
        return

    # Display current item details
    st.subheader(f"Editing Item: {item[2]}")  # item[2] is the name

    # Create form with current values
    with st.form("edit_item_form"):
        code = st.text_input("Item Code (must be unique)", value=item[1])
        name = st.text_input("Item Name", value=item[2])
        category = st.text_input("Category", value=item[3] if item[3] else "")
        location = st.text_input("Storage Location", value=item[4] if item[4] else "")
        description = st.text_area("Description", value=item[5] if item[5] else "")

        submit_button = st.form_submit_button("Update Item")

        if submit_button:
            if not code or not name:
                st.error("Code and Name are required fields")
            else:
                success, message = db.update_item(item_id, code, name, category, location, description)
                if success:
                    st.success(message)
                    # Navigate back to dashboard
                    admin_navigate_to("dashboard")
                else:
                    st.error(message)

# Borrowing History Page
def show_borrowing_history():
    st.title("Borrowing History")

    # Create a sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        st.button("Back to Dashboard", on_click=admin_navigate_to, args=("dashboard",))
        st.button("Logout", on_click=admin_logout)

    # Get borrowing history from database
    history = db.get_borrowing_history()

    if not history:
        st.info("No borrowing history found.")
    else:
        # Convert to DataFrame for better display
        df = pd.DataFrame(history, columns=["ID", "User", "Item Code", "Item Name", "Borrow Date", "Return Date"])

        # Add a status column
        df["Status"] = df["Return Date"].apply(lambda x: "Returned" if x else "Borrowed")

        # Reorder columns for better display
        df = df[["ID", "User", "Item Code", "Item Name", "Borrow Date", "Return Date", "Status"]]

        # Display the dataframe
        st.dataframe(df)

# Main admin app logic
def main():
    # Check if admin is logged in
    if not st.session_state.admin_logged_in:
        show_admin_login()
    else:
        # Show the appropriate page based on session state
        if st.session_state.admin_page == "dashboard":
            show_admin_dashboard()
        elif st.session_state.admin_page == "add_item":
            show_add_item()
        elif st.session_state.admin_page == "edit_item":
            show_edit_item()
        elif st.session_state.admin_page == "borrowing_history":
            show_borrowing_history()

if __name__ == "__main__":
    main()
