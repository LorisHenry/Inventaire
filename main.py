import streamlit as st
import pandas as pd
import os
from database import Database

# Translations dictionary
translations = {
    "en": {
        # Main interface
        "app_title": "Inventory Management System",
        "welcome": "Welcome to the Inventory Management System. Please select an interface:",
        "user_interface": "User Interface",
        "for_borrowing": "For borrowing and returning items",
        "admin_interface": "Admin Interface",
        "for_managing": "For managing inventory and viewing reports",
        "launch_user": "Launch User Interface",
        "launch_admin": "Launch Admin Interface",
        "copyright": "© 2023 Inventory Management System",
        "theme_dark": "Dark",
        "theme_light": "Light",

        # Login
        "login_register": "Login or Register",
        "username": "Username",
        "password": "Password",
        "login_button": "Login / Register",
        "back_to_main": "Back to Main Menu",

        # User dashboard
        "welcome_user": "Welcome, {}!",
        "navigation": "Navigation",
        "borrow_item": "Borrow Item",
        "logout": "Logout",
        "available_items": "Available Items",
        "your_borrowed": "Your Borrowed Items",
        "search_items": "Search items",
        "filter_category": "Filter by category",
        "all_categories": "All Categories",
        "no_items_match": "No items match your search criteria.",
        "category": "Category",
        "borrow": "Borrow",
        "no_borrowed": "You don't have any borrowed items.",
        "code": "Code:",
        "borrowed_on": "Borrowed on:",
        "return": "Return",

        # Admin
        "admin_title": "Inventory Admin Dashboard",
        "add_new_item": "Add New Item",
        "view_history": "View Borrowing History",
        "active_borrowers": "Active Borrowers",
        "current_inventory": "Current Inventory",
        "borrowed_items": "Borrowed Items",
        "no_inventory": "No items in the inventory.",
        "item_actions": "Item Actions",
        "edit_item_id": "Enter Item ID to Edit",
        "edit_item": "Edit Item",
        "delete_item_id": "Enter Item ID to Delete",
        "delete_item": "Delete Item",
        "currently_borrowed": "Currently Borrowed Items",
        "no_borrowed_items": "No items are currently borrowed.",
        "status": "Status",
        "filter_by_user": "Filter by User",
        "select_user": "Select a user",
        "all_users": "All Users",

        # Active borrowers
        "users_active": "Users with Active Borrowings",
        "click_user": "Click on a user to see their active borrowings.",
        "no_active_users": "No users have active borrowings.",
        "active_borrowings": "Active borrowings:",
        "view_borrowings": "View Borrowings",
        "borrowings_for": "Borrowings for {}",
        "back_to_borrowers": "Back to Active Borrowers",
        "back_to_dashboard": "Back to Dashboard",
        "no_active_borrowings": "{} has no active borrowings.",

        # Add/Edit item
        "add_item_title": "Add New Item",
        "edit_item_title": "Edit Item",
        "item_code": "Item Code (must be unique)",
        "item_name": "Item Name",
        "item_category": "Category",
        "storage_location": "Storage Location",
        "description": "Description",
        "choose_image": "Choose an image for the item",
        "add_item_button": "Add Item",
        "required_fields": "Code and Name are required fields",
        "item_added": "Item '{}' added successfully!",
        "add_failed": "Failed to add item. Code might already exist.",
        "editing_item": "Editing Item: {}",
        "current_image": "Current Image",
        "upload_new": "Upload a new image (leave empty to keep the current image)",
        "update_item": "Update Item",

        # Borrowing history
        "borrowing_history": "Borrowing History",
        "no_history": "No borrowing history found.",
        "borrowed": "Borrowed",
        "returned": "Returned"
    },
    "fr": {
        # Main interface
        "app_title": "Système de Gestion d'Inventaire",
        "welcome": "Bienvenue dans le Système de Gestion d'Inventaire. Veuillez sélectionner une interface :",
        "user_interface": "Interface Utilisateur",
        "for_borrowing": "Pour emprunter et retourner des articles",
        "admin_interface": "Interface Administrateur",
        "for_managing": "Pour gérer l'inventaire et consulter les rapports",
        "launch_user": "Lancer l'Interface Utilisateur",
        "launch_admin": "Lancer l'Interface Administrateur",
        "copyright": "© 2023 Système de Gestion d'Inventaire",
        "theme_dark": "Sombre",
        "theme_light": "Clair",

        # Login
        "login_register": "Connexion ou Inscription",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "login_button": "Connexion / Inscription",
        "back_to_main": "Retour au Menu Principal",

        # User dashboard
        "welcome_user": "Bienvenue, {} !",
        "navigation": "Navigation",
        "borrow_item": "Emprunter un Article",
        "logout": "Déconnexion",
        "available_items": "Articles Disponibles",
        "your_borrowed": "Vos Articles Empruntés",
        "search_items": "Rechercher des articles",
        "filter_category": "Filtrer par catégorie",
        "all_categories": "Toutes les Catégories",
        "no_items_match": "Aucun article ne correspond à vos critères de recherche.",
        "category": "Catégorie",
        "borrow": "Emprunter",
        "no_borrowed": "Vous n'avez pas d'articles empruntés.",
        "code": "Code :",
        "borrowed_on": "Emprunté le :",
        "return": "Retourner",

        # Admin
        "admin_title": "Tableau de Bord Administrateur",
        "add_new_item": "Ajouter un Nouvel Article",
        "view_history": "Voir l'Historique des Emprunts",
        "active_borrowers": "Emprunteurs Actifs",
        "current_inventory": "Inventaire Actuel",
        "borrowed_items": "Articles Empruntés",
        "no_inventory": "Aucun article dans l'inventaire.",
        "item_actions": "Actions sur les Articles",
        "edit_item_id": "Entrez l'ID de l'article à modifier",
        "edit_item": "Modifier l'Article",
        "delete_item_id": "Entrez l'ID de l'article à supprimer",
        "delete_item": "Supprimer l'Article",
        "currently_borrowed": "Articles Actuellement Empruntés",
        "no_borrowed_items": "Aucun article n'est actuellement emprunté.",
        "status": "Statut",
        "filter_by_user": "Filtrer par Utilisateur",
        "select_user": "Sélectionnez un utilisateur",
        "all_users": "Tous les Utilisateurs",

        # Active borrowers
        "users_active": "Utilisateurs avec des Emprunts Actifs",
        "click_user": "Cliquez sur un utilisateur pour voir ses emprunts actifs.",
        "no_active_users": "Aucun utilisateur n'a d'emprunts actifs.",
        "active_borrowings": "Emprunts actifs :",
        "view_borrowings": "Voir les Emprunts",
        "borrowings_for": "Emprunts pour {}",
        "back_to_borrowers": "Retour aux Emprunteurs Actifs",
        "back_to_dashboard": "Retour au Tableau de Bord",
        "no_active_borrowings": "{} n'a pas d'emprunts actifs.",

        # Add/Edit item
        "add_item_title": "Ajouter un Nouvel Article",
        "edit_item_title": "Modifier l'Article",
        "item_code": "Code de l'Article (doit être unique)",
        "item_name": "Nom de l'Article",
        "item_category": "Catégorie",
        "storage_location": "Emplacement de Stockage",
        "description": "Description",
        "choose_image": "Choisissez une image pour l'article",
        "add_item_button": "Ajouter l'Article",
        "required_fields": "Les champs Code et Nom sont obligatoires",
        "item_added": "L'article '{}' a été ajouté avec succès !",
        "add_failed": "Échec de l'ajout de l'article. Le code existe peut-être déjà.",
        "editing_item": "Modification de l'Article : {}",
        "current_image": "Image Actuelle",
        "upload_new": "Télécharger une nouvelle image (laissez vide pour conserver l'image actuelle)",
        "update_item": "Mettre à Jour l'Article",

        # Borrowing history
        "borrowing_history": "Historique des Emprunts",
        "no_history": "Aucun historique d'emprunt trouvé.",
        "borrowed": "Emprunté",
        "returned": "Retourné"
    }
}

# Initialize language and theme in session state
if 'language' not in st.session_state:
    st.session_state.language = "en"
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"  # Default to dark theme

# Function to get text in the current language
def get_text(key):
    return translations[st.session_state.language].get(key, key)

# Function to get CSS based on the current theme
def get_theme_css():
    if st.session_state.theme == "light":
        return """
        <style>
        .main {
            background-color: white;
        }
        .stApp {
            background-color: white;
        }
        .stButton>button {
            background-color: #f0f2f6;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
        .stTextInput>div>div>input {
            background-color: #f0f2f6;
        }
        </style>
        """
    else:
        return """
        <style>
        .stButton>button {
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
        </style>
        """

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
def login(username, password):
    if username.strip() == "":
        st.error("Please enter a username")
        return

    if password.strip() == "":
        st.error("Please enter a password")
        return

    # Check if user exists
    user = db.get_user_by_username(username)

    if user:
        # Existing user - authenticate
        user_id = db.authenticate_user(username, password)
        if user_id:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_id = user_id
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid password. Please try again.")
    else:
        # New user - register
        user_id = db.add_user(username, password)
        if user_id:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_id = user_id
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Registration failed. Please try again.")

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

# Function to switch language
def switch_language(lang):
    st.session_state.language = lang
    st.rerun()

# Function to switch theme
def switch_theme(theme):
    st.session_state.theme = theme
    st.rerun()

# Main interface
def show_main_interface():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("app_title"))

    st.write(get_text("welcome"))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(get_text("user_interface"))
        st.write(get_text("for_borrowing"))
        if st.button(get_text("launch_user"), key="user"):
            switch_interface("user")

    with col2:
        st.subheader(get_text("admin_interface"))
        st.write(get_text("for_managing"))
        if st.button(get_text("launch_admin"), key="admin"):
            switch_interface("admin")

    st.markdown("---")
    st.write(get_text("copyright"))

# User Login Page
def show_login_page():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("app_title"))

    st.subheader(get_text("login_register"))

    with st.form("login_form"):
        username = st.text_input(get_text("username"))
        password = st.text_input(get_text("password"), type="password")
        submit_button = st.form_submit_button(get_text("login_button"))

        if submit_button:
            login(username, password)

    # Add a back button to return to the main interface
    if st.button(get_text("back_to_main")):
        switch_interface("main")

# User Dashboard Page
def show_dashboard():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("welcome_user").format(st.session_state.username))

    # Create a sidebar for navigation
    with st.sidebar:
        st.title(get_text("navigation"))
        st.button(get_text("borrow_item"), on_click=navigate_to, args=("borrow",))
        st.button(get_text("logout"), on_click=logout)

    # Add tabs for available items and borrowed items
    tab1, tab2 = st.tabs([get_text("available_items"), get_text("your_borrowed")])

    with tab1:
        st.header(get_text("available_items"))

        # Get all available items
        items = db.get_all_items()
        available_items = [item for item in items if item[7] == 1]  # item[7] is the available field

        # Add search and filter functionality
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input(get_text("search_items"), "")
        with col2:
            # Get unique categories
            categories = list(set([item[3] for item in items if item[3]]))
            categories.insert(0, get_text("all_categories"))
            selected_category = st.selectbox(get_text("filter_category"), categories)

        # Filter items based on search and category
        filtered_items = []
        for item in available_items:
            item_id, code, name, category, location, description, image_path, available = item

            # Apply search filter
            if search_term and search_term.lower() not in name.lower() and (not description or search_term.lower() not in description.lower()):
                continue

            # Apply category filter
            if selected_category != get_text("all_categories") and category != selected_category:
                continue

            filtered_items.append(item)

        if not filtered_items:
            st.info(get_text("no_items_match"))
        else:
            # Display items in a grid layout (5 items per row)
            cols = st.columns(5)
            for i, item in enumerate(filtered_items):
                item_id, code, name, category, location, description, image_path, available = item
                with cols[i % 5]:
                    # Display item image
                    if image_path and os.path.exists(image_path):
                        st.image(image_path, use_column_width=True)
                    else:
                        # Display placeholder image
                        st.image("https://via.placeholder.com/150", use_column_width=True)

                    # Display item details
                    st.write(f"**{name}**")
                    st.write(f"{get_text('category')}: {category if category else 'N/A'}")

                    # Add borrow button
                    if st.button(get_text("borrow"), key=f"borrow_{code}"):
                        success, message = db.borrow_item(st.session_state.user_id, code)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

    with tab2:
        st.header(get_text("your_borrowed"))

        # Get user's borrowed items
        borrowed_items = db.get_user_borrowings(st.session_state.user_id)

        if not borrowed_items:
            st.info(get_text("no_borrowed"))
        else:
            # Create a table to display borrowed items
            for item in borrowed_items:
                borrowing_id, code, name, category, borrow_date = item

                # Create a card-like display for each item
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.subheader(name)
                    st.write(f"**{get_text('code')}** {code}")
                    if category:
                        st.write(f"**{get_text('category')}:** {category}")

                with col2:
                    st.write(f"**{get_text('borrowed_on')}** {borrow_date}")

                with col3:
                    st.button(get_text("return"), key=f"return_{borrowing_id}", 
                            on_click=return_item, args=(borrowing_id,))

                st.markdown("---")

# Borrow Item Page
def show_borrow_page():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("borrow_item"))

    # Create a sidebar for navigation
    with st.sidebar:
        st.title(get_text("navigation"))
        st.button(get_text("back_to_dashboard"), on_click=navigate_to, args=("dashboard",))
        st.button(get_text("logout"), on_click=logout)

    st.write(get_text("item_code"))

    with st.form("borrow_form"):
        item_code = st.text_input(get_text("item_code"))
        submit_button = st.form_submit_button(get_text("borrow"))

        if submit_button:
            borrow_item(item_code)

# Admin Login Page
def show_admin_login():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("admin_interface"))

    st.subheader(get_text("login_register"))

    with st.form("admin_login_form"):
        username = st.text_input(get_text("username"))
        password = st.text_input(get_text("password"), type="password")
        submit_button = st.form_submit_button(get_text("login_button"))

        if submit_button:
            admin_login(username, password)

    # Add a back button to return to the main interface
    if st.button(get_text("back_to_main")):
        switch_interface("main")

# Admin Dashboard
def show_admin_dashboard():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("admin_title"))

    # Create a sidebar for navigation
    with st.sidebar:
        st.title(get_text("navigation"))
        st.button(get_text("add_new_item"), on_click=admin_navigate_to, args=("add_item",))
        st.button(get_text("view_history"), on_click=admin_navigate_to, args=("borrowing_history",))
        st.button(get_text("active_borrowers"), on_click=admin_navigate_to, args=("active_borrowers",))
        st.button(get_text("logout"), on_click=admin_logout)

    # Create tabs for different views
    tab1, tab2 = st.tabs([get_text("current_inventory"), get_text("borrowed_items")])

    with tab1:
        st.header(get_text("current_inventory"))

        # Get all items from the database
        items = db.get_all_items()

        if not items:
            st.info(get_text("no_inventory"))
        else:
            # Convert to DataFrame for better display
            df = pd.DataFrame(items, columns=["ID", "Code", "Name", "Category", "Location", "Description", "Image Path", "Available"])

            # Replace boolean values with more readable text
            df["Available"] = df["Available"].map({1: "Yes", 0: "No"})

            # Add search functionality
            search_term = st.text_input(get_text("search_items"), "")
            if search_term:
                df = df[df["Name"].str.contains(search_term, case=False) | 
                        df["Description"].str.contains(search_term, case=False, na=False) |
                        df["Code"].str.contains(search_term, case=False)]

            # Display the dataframe
            st.dataframe(df)

            st.subheader(get_text("item_actions"))
            col1, col2 = st.columns(2)

            with col1:
                item_id = st.number_input(get_text("edit_item_id"), min_value=1, step=1)
                st.button(get_text("edit_item"), on_click=set_edit_item, args=(item_id,))

            with col2:
                delete_id = st.number_input(get_text("delete_item_id"), min_value=1, step=1)
                if st.button(get_text("delete_item")):
                    success, message = db.delete_item(delete_id)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

    with tab2:
        st.header(get_text("currently_borrowed"))

        # Get borrowing history
        history = db.get_borrowing_history()

        # Filter for active borrowings
        active_borrowings = [item for item in history if item[5] is None]

        if not active_borrowings:
            st.info(get_text("no_borrowed_items"))
        else:
            # Convert to DataFrame for better display
            df = pd.DataFrame(active_borrowings, columns=["ID", "User", "Item Code", "Item Name", "Borrow Date", "Return Date"])

            # Add a status column
            df["Status"] = get_text("borrowed")

            # Reorder columns for better display
            df = df[["ID", "User", "Item Code", "Item Name", "Borrow Date", "Status"]]

            # Display the dataframe
            st.dataframe(df)

            # Add option to filter by user
            st.subheader(get_text("filter_by_user"))
            users = list(set(df["User"].tolist()))
            selected_user = st.selectbox(get_text("select_user"), [get_text("all_users")] + users)

            if selected_user != get_text("all_users"):
                filtered_df = df[df["User"] == selected_user]
                st.dataframe(filtered_df)

# Add Item Page
def show_add_item():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("add_item_title"))

    # Create a sidebar for navigation
    with st.sidebar:
        st.title(get_text("navigation"))
        st.button(get_text("back_to_dashboard"), on_click=admin_navigate_to, args=("dashboard",))
        st.button(get_text("logout"), on_click=admin_logout)

    with st.form("add_item_form"):
        code = st.text_input(get_text("item_code"))
        name = st.text_input(get_text("item_name"))
        category = st.text_input(get_text("item_category"))
        location = st.text_input(get_text("storage_location"))
        description = st.text_area(get_text("description"))

        # Image upload
        uploaded_file = st.file_uploader(get_text("choose_image"), type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button(get_text("add_item_button"))

        if submit_button:
            if not code or not name:
                st.error(get_text("required_fields"))
            else:
                # Handle image upload
                image_path = None
                if uploaded_file is not None:
                    # Create images directory if it doesn't exist
                    if not os.path.exists("images"):
                        os.makedirs("images")

                    # Save the uploaded file
                    image_path = f"images/{code}_{uploaded_file.name}"
                    with open(image_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                success = db.add_item(code, name, category, location, description, image_path)
                if success:
                    st.success(get_text("item_added").format(name))
                    # Clear form fields by navigating back to the same page
                    admin_navigate_to("add_item")
                else:
                    st.error(get_text("add_failed"))

# Edit Item Page
def show_edit_item():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("edit_item_title"))

    # Create a sidebar for navigation
    with st.sidebar:
        st.title(get_text("navigation"))
        st.button(get_text("back_to_dashboard"), on_click=admin_navigate_to, args=("dashboard",))
        st.button(get_text("logout"), on_click=admin_logout)

    item_id = st.session_state.edit_item_id

    # Get the item details
    item = db.get_item_by_id(item_id)

    if not item:
        st.error(f"Item with ID {item_id} not found")
        st.button(get_text("back_to_dashboard"), on_click=admin_navigate_to, args=("dashboard",))
        return

    # Display current item details
    st.subheader(get_text("editing_item").format(item[2]))  # item[2] is the name

    # Display current image if it exists
    current_image_path = item[6] if len(item) > 6 and item[6] else None
    if current_image_path and os.path.exists(current_image_path):
        st.image(current_image_path, caption=get_text("current_image"), width=300)

    # Create form with current values
    with st.form("edit_item_form"):
        code = st.text_input(get_text("item_code"), value=item[1])
        name = st.text_input(get_text("item_name"), value=item[2])
        category = st.text_input(get_text("item_category"), value=item[3] if item[3] else "")
        location = st.text_input(get_text("storage_location"), value=item[4] if item[4] else "")
        description = st.text_area(get_text("description"), value=item[5] if item[5] else "")

        # Image upload
        st.write(get_text("upload_new"))
        uploaded_file = st.file_uploader(get_text("choose_image"), type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button(get_text("update_item"))

        if submit_button:
            if not code or not name:
                st.error(get_text("required_fields"))
            else:
                # Handle image upload
                image_path = current_image_path
                if uploaded_file is not None:
                    # Create images directory if it doesn't exist
                    if not os.path.exists("images"):
                        os.makedirs("images")

                    # Save the uploaded file
                    image_path = f"images/{code}_{uploaded_file.name}"
                    with open(image_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                success, message = db.update_item(item_id, code, name, category, location, description, image_path)
                if success:
                    st.success(message)
                    # Navigate back to dashboard
                    admin_navigate_to("dashboard")
                else:
                    st.error(message)

# Borrowing History Page
def show_borrowing_history():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("borrowing_history"))

    # Create a sidebar for navigation
    with st.sidebar:
        st.title(get_text("navigation"))
        st.button(get_text("back_to_dashboard"), on_click=admin_navigate_to, args=("dashboard",))
        st.button(get_text("logout"), on_click=admin_logout)

    # Get borrowing history from database
    history = db.get_borrowing_history()

    if not history:
        st.info(get_text("no_history"))
    else:
        # Convert to DataFrame for better display
        df = pd.DataFrame(history, columns=["ID", "User", "Item Code", "Item Name", "Borrow Date", "Return Date"])

        # Add a status column
        df["Status"] = df["Return Date"].apply(lambda x: get_text("returned") if x else get_text("borrowed"))

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

# Active Borrowers Page
def show_active_borrowers():
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("users_active"))

    # Create a sidebar for navigation
    with st.sidebar:
        st.title(get_text("navigation"))
        st.button(get_text("back_to_dashboard"), on_click=admin_navigate_to, args=("dashboard",))
        st.button(get_text("logout"), on_click=admin_logout)

    # Get users with active borrowings
    users = db.get_users_with_active_borrowings()

    if not users:
        st.info(get_text("no_active_users"))
    else:
        st.write(get_text("click_user"))

        # Display users in a table
        for user_id, username, borrow_count in users:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(username)
                st.write(f"{get_text('active_borrowings')} {borrow_count}")

            with col2:
                if st.button(get_text("view_borrowings"), key=f"view_{user_id}"):
                    st.session_state.selected_user_id = user_id
                    st.session_state.selected_username = username
                    admin_navigate_to("user_borrowings")

            st.markdown("---")

# User Borrowings Page
def show_user_borrowings():
    user_id = st.session_state.selected_user_id
    username = st.session_state.selected_username

    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)

    # Language and theme selectors in the top right
    col1, col2, col3 = st.columns([5, 1, 1])

    with col2:
        lang = st.selectbox("", ["English", "Français"], 
                           index=0 if st.session_state.language == "en" else 1,
                           key="lang_select")
        if lang == "English" and st.session_state.language != "en":
            switch_language("en")
        elif lang == "Français" and st.session_state.language != "fr":
            switch_language("fr")

    with col3:
        theme = st.selectbox("", [get_text("theme_dark"), get_text("theme_light")], 
                           index=0 if st.session_state.theme == "dark" else 1,
                           key="theme_select")
        if theme == get_text("theme_dark") and st.session_state.theme != "dark":
            switch_theme("dark")
        elif theme == get_text("theme_light") and st.session_state.theme != "light":
            switch_theme("light")

    with col1:
        st.title(get_text("borrowings_for").format(username))

    # Create a sidebar for navigation
    with st.sidebar:
        st.title(get_text("navigation"))
        st.button(get_text("back_to_borrowers"), on_click=admin_navigate_to, args=("active_borrowers",))
        st.button(get_text("back_to_dashboard"), on_click=admin_navigate_to, args=("dashboard",))
        st.button(get_text("logout"), on_click=admin_logout)

    # Get borrowings for this user
    borrowings = db.get_borrowings_by_user(user_id)

    # Filter for active borrowings
    active_borrowings = [b for b in borrowings if b[5] is None]

    if not active_borrowings:
        st.info(get_text("no_active_borrowings").format(username))
    else:
        st.subheader(get_text("active_borrowings"))

        # Display borrowings in a table
        for borrowing_id, code, name, category, borrow_date, _ in active_borrowings:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(name)
                st.write(f"**{get_text('code')}** {code}")
                if category:
                    st.write(f"**{get_text('category')}:** {category}")
                st.write(f"**{get_text('borrowed_on')}** {borrow_date}")

            st.markdown("---")

# Admin Interface
def show_admin_interface():

    # Initialize session state variables for user borrowings if they don't exist
    if 'selected_user_id' not in st.session_state:
        st.session_state.selected_user_id = None
    if 'selected_username' not in st.session_state:
        st.session_state.selected_username = None

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
        elif st.session_state.admin_page == "active_borrowers":
            show_active_borrowers()
        elif st.session_state.admin_page == "user_borrowings":
            show_user_borrowings()

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
