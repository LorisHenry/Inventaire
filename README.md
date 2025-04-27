# Inventory Management System

A local inventory management system for libraries, classrooms, or any small-scale inventory tracking needs. This application allows users to borrow and return items, while administrators can manage the inventory.

## Features

### User Interface
- Simple login with username (no password required)
- View currently borrowed items
- Return items with a single click
- Borrow new items by entering their unique code

### Admin Interface
- Secure login with username and password
- View all inventory items
- Add new items to the inventory
- Edit existing items
- Delete items (with safety checks)
- View complete borrowing history

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/inventory-management.git
cd inventory-management
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

1. Run the main application:
```
streamlit run main.py
```

2. Choose between the User Interface or Admin Interface:
   - **User Interface**: For borrowing and returning items
   - **Admin Interface**: For managing inventory and viewing reports

The application uses a single integrated interface that allows you to switch between user and admin modes without restarting the application.

### User Interface
1. Enter your username to log in
2. View your currently borrowed items
3. Return items by clicking the "Return" button
4. Borrow new items by clicking "Borrow Item" and entering the item's unique code

### Admin Interface
1. Log in with the admin credentials:
   - Username: `admin`
   - Password: `admin`
2. View the current inventory
3. Add new items with the "Add New Item" button
4. Edit or delete existing items using their ID
5. View borrowing history with the "View Borrowing History" button

## Database

The application uses SQLite for data storage, which is stored locally in a file named `inventory.db`. The database includes tables for:
- Items (with unique codes)
- Users
- Borrowing transactions

## Security Note

This application is designed for local use in trusted environments. The admin credentials are hardcoded and there is no password required for user login. In a production environment, you would want to implement proper authentication and authorization.

## Customization

You can customize the application by:
- Modifying the database schema in `database.py`
- Adding new features to the user or admin interfaces
- Implementing additional security measures

## License

This project is licensed under the MIT License - see the LICENSE file for details.
