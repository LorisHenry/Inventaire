import streamlit as st
import pandas as pd
from database import Database

# Set page configuration once at the beginning
st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📚",
    layout="wide"
)

# Initialize the database
db = Database()

# Initialize session state variables if they don't exist
if 'interface' not in st.session_state:
    st.session_state.interface = "main"  # main, user, admin

# User interface session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'page' not in st.session_state:
    st.session_state.page = "login"

# Admin interface session state
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'admin_page' not in st.session_state:
    st.session_state.admin_page = "login"
if 'edit_item_id' not in st.session_state:
    st.session_state.edit_item_id = None

# Simple admin authentication
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminkeya"

# Function to switch between interfaces
def switch_interface(interface):
    st.session_state.interface = interface
    st.rerun()

# Function to handle user login
def login(username):
    if username.strip() == "":
        st.error("Please enter a username")
        return

    # Add user to database or get existing user ID
    user_id = db.add_user(username)

    if user_id:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_id = user_id
        st.session_state.page = "dashboard"
        st.rerun()
    else:
        st.error("Login failed. Please try again.")

# Function to handle user logout
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_id = None
    st.session_state.page = "login"
    switch_interface("main")

# Function to navigate between user pages
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Function to handle item return
def return_item(borrowing_id):
    success, message = db.return_item(borrowing_id)
    if success:
        st.success(message)
        st.rerun()
    else:
        st.error(message)

# Function to handle item borrowing
def borrow_item(item_code):
    if not item_code.strip():
        st.error("Please enter an item code")
        return

    success, message = db.borrow_item(st.session_state.user_id, item_code)
    if success:
        st.success(message)
        navigate_to("dashboard")
    else:
        st.error(message)

# Function to handle admin login
def admin_login(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.session_state.admin_logged_in = True
        st.session_state.admin_page = "dashboard"
        st.rerun()
    else:
        st.error("Invalid username or password")

# Function to handle admin logout
def admin_logout():
    st.session_state.admin_logged_in = False
    st.session_state.admin_page = "login"
    switch_interface("main")

# Function to navigate between admin pages
def admin_navigate_to(page):
    st.session_state.admin_page = page
    st.rerun()

# Function to set item for editing
def set_edit_item(item_id):
    st.session_state.edit_item_id = item_id
    admin_navigate_to("edit_item")

# Main interface
def show_main_interface():

    st.title("Inventory Management System")
    st.write("Welcome to the Inventory Management System. Please select an interface:")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("User Interface")
        st.write("For borrowing and returning items")
        if st.button("Launch User Interface", key="user"):
            switch_interface("user")

    with col2:
        st.subheader("Admin Interface")
        st.write("For managing inventory and viewing reports")
        if st.button("Launch Admin Interface", key="admin"):
            switch_interface("admin")

    st.markdown("---")
    st.write("© 2023 Inventory Management System")

# User Login Page
def show_login_page():
    st.title("Inventory Management System")
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            login(username)

    # Add a back button to return to the main interface
    if st.button("Back to Main Menu"):
        switch_interface("main")

# User Dashboard Page
def show_dashboard():
    st.title(f"Welcome, {st.session_state.username}!")

    # Create a sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        st.button("Borrow Item", on_click=navigate_to, args=("borrow",))
        st.button("Logout", on_click=logout)

    st.header("Your Borrowed Items")

    # Get user's borrowed items
    borrowed_items = db.get_user_borrowings(st.session_state.user_id)

    if not borrowed_items:
        st.info("You don't have any borrowed items.")
    else:
        # Create a table to display borrowed items
        for item in borrowed_items:
            borrowing_id, code, name, category, borrow_date = item

            # Create a card-like display for each item
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.subheader(name)
                st.write(f"**Code:** {code}")
                if category:
                    st.write(f"**Category:** {category}")

            with col2:
                st.write(f"**Borrowed on:** {borrow_date}")

            with col3:
                st.button(f"Return", key=f"return_{borrowing_id}", 
                          on_click=return_item, args=(borrowing_id,))

            st.markdown("---")

# Borrow Item Page
def show_borrow_page():
    st.title("Borrow an Item")

    # Create a sidebar for navigation
    with st.sidebar:
        st.title("Navigation")
        st.button("Back to Dashboard", on_click=navigate_to, args=("dashboard",))
        st.button("Logout", on_click=logout)

    st.write("Enter the unique code of the item you want to borrow:")

    with st.form("borrow_form"):
        item_code = st.text_input("Item Code")
        submit_button = st.form_submit_button("Borrow")

        if submit_button:
            borrow_item(item_code)

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

    # Add a back button to return to the main interface
    if st.button("Back to Main Menu"):
        switch_interface("main")

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
                    st.rerun()
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

# User Interface
def show_user_interface():

    # Check if user is logged in
    if not st.session_state.logged_in:
        show_login_page()
    else:
        # Show the appropriate page based on session state
        if st.session_state.page == "dashboard":
            show_dashboard()
        elif st.session_state.page == "borrow":
            show_borrow_page()

# Admin Interface
def show_admin_interface():

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

def main():
    # Determine which interface to show
    if st.session_state.interface == "main":
        show_main_interface()
    elif st.session_state.interface == "user":
        show_user_interface()
    elif st.session_state.interface == "admin":
        show_admin_interface()

if __name__ == "__main__":
    main()
