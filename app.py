import streamlit as st
import sqlite3
from database import Database

# Initialize the database
db = Database()

# Set page configuration
st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📚",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'page' not in st.session_state:
    st.session_state.page = "login"

# Function to handle login
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
        st.experimental_rerun()
    else:
        st.error("Login failed. Please try again.")

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_id = None
    st.session_state.page = "login"
    st.experimental_rerun()

# Function to navigate between pages
def navigate_to(page):
    st.session_state.page = page
    st.experimental_rerun()

# Function to handle item return
def return_item(borrowing_id):
    success, message = db.return_item(borrowing_id)
    if success:
        st.success(message)
        st.experimental_rerun()
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

# Login Page
def show_login_page():
    st.title("Inventory Management System")
    st.subheader("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            login(username)

# Dashboard Page
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

# Main app logic
def main():
    # Check if user is logged in
    if not st.session_state.logged_in:
        show_login_page()
    else:
        # Show the appropriate page based on session state
        if st.session_state.page == "dashboard":
            show_dashboard()
        elif st.session_state.page == "borrow":
            show_borrow_page()

if __name__ == "__main__":
    main()