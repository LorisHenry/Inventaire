import sqlite3
import os
import threading
from datetime import datetime

class Database:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_name="inventory.db"):
        """Singleton pattern to ensure only one database connection"""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance.db_name = db_name
                cls._instance.conn = None
                cls._instance.cursor = None
                cls._instance.connect(with_lock=False)
                cls._instance.create_tables(with_lock=False)
        return cls._instance

    def __init__(self, db_name="inventory.db"):
        """Initialize the database connection"""
        # The initialization is done in __new__
        pass

    def connect(self, with_lock=True):
        """Connect to the SQLite database"""
        def _connect():
            print("toast")
            try:
                if self.conn is None:
                    self.conn = sqlite3.connect(self.db_name)
                    self.cursor = self.conn.cursor()
                    print(f"Connected to {self.db_name}")
            except sqlite3.Error as e:
                print(f"Error connecting to database: {e}")

        if with_lock:
            with self.__class__._lock:
                _connect()
        else:
            _connect()

    def create_tables(self, with_lock=True):
        """Create the necessary tables if they don't exist"""
        def _create_tables():
            try:
                # Create Items table
                self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT,
                    location TEXT,
                    description TEXT,
                    available BOOLEAN DEFAULT 1
                )
                ''')

                # Create Users table
                self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL
                )
                ''')

                # Create Borrowings table
                self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS borrowings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    item_id INTEGER NOT NULL,
                    borrow_date TEXT NOT NULL,
                    return_date TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (item_id) REFERENCES items (id)
                )
                ''')

                self.conn.commit()
                print("Tables created successfully")
            except sqlite3.Error as e:
                print(f"Error creating tables: {e}")
                try:
                    self.conn.rollback()
                except:
                    pass

        if with_lock:
            with self.__class__._lock:
                _create_tables()
        else:
            _create_tables()

    def add_item(self, code, name, category=None, location=None, description=None):
        """Add a new item to the inventory"""
        try:
            self.cursor.execute('''
            INSERT INTO items (code, name, category, location, description)
            VALUES (?, ?, ?, ?, ?)
            ''', (code, name, category, location, description))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding item: {e}")
            return False

    def get_item_by_code(self, code):
        """Get an item by its unique code"""
        try:
            self.cursor.execute('SELECT * FROM items WHERE code = ?', (code,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting item: {e}")
            return None

    def get_all_items(self):
        """Get all items in the inventory"""
        try:
            self.cursor.execute('SELECT * FROM items')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting items: {e}")
            return []

    def add_user(self, username):
        """Add a new user or get existing user"""
        with self.__class__._lock:
            try:
                # Check if user exists
                self.cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
                user = self.cursor.fetchone()

                if user:
                    return user[0]  # Return existing user ID

                # Add new user
                self.cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
                self.conn.commit()
                return self.cursor.lastrowid
            except sqlite3.Error as e:
                print(f"Error adding user: {e}")
                # Try to rollback if possible
                try:
                    self.conn.rollback()
                except:
                    pass
                return None

    def get_user_by_username(self, username):
        """Get a user by username"""
        try:
            self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting user: {e}")
            return None

    def borrow_item(self, user_id, item_code):
        """Record a borrowing transaction"""
        try:
            # Get item ID from code
            self.cursor.execute('SELECT id, available FROM items WHERE code = ?', (item_code,))
            item = self.cursor.fetchone()

            if not item:
                return False, "Item not found"

            item_id, available = item

            if not available:
                return False, "Item is not available"

            # Mark item as unavailable
            self.cursor.execute('UPDATE items SET available = 0 WHERE id = ?', (item_id,))

            # Record borrowing
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute('''
            INSERT INTO borrowings (user_id, item_id, borrow_date)
            VALUES (?, ?, ?)
            ''', (user_id, item_id, current_date))

            self.conn.commit()
            return True, "Item borrowed successfully"
        except sqlite3.Error as e:
            print(f"Error borrowing item: {e}")
            return False, f"Database error: {e}"

    def return_item(self, borrowing_id):
        """Record a return transaction"""
        try:
            # Get the item_id from borrowing
            self.cursor.execute('SELECT item_id FROM borrowings WHERE id = ?', (borrowing_id,))
            result = self.cursor.fetchone()

            if not result:
                return False, "Borrowing record not found"

            item_id = result[0]

            # Mark item as available
            self.cursor.execute('UPDATE items SET available = 1 WHERE id = ?', (item_id,))

            # Update borrowing record with return date
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute('''
            UPDATE borrowings SET return_date = ? WHERE id = ?
            ''', (current_date, borrowing_id))

            self.conn.commit()
            return True, "Item returned successfully"
        except sqlite3.Error as e:
            print(f"Error returning item: {e}")
            return False, f"Database error: {e}"

    def get_user_borrowings(self, user_id):
        """Get all active borrowings for a user"""
        try:
            self.cursor.execute('''
            SELECT b.id, i.code, i.name, i.category, b.borrow_date
            FROM borrowings b
            JOIN items i ON b.item_id = i.id
            WHERE b.user_id = ? AND b.return_date IS NULL
            ''', (user_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting user borrowings: {e}")
            return []

    def update_item(self, item_id, code, name, category=None, location=None, description=None):
        """Update an existing item in the inventory"""
        try:
            # Check if the code already exists for a different item
            self.cursor.execute('SELECT id FROM items WHERE code = ? AND id != ?', (code, item_id))
            existing_item = self.cursor.fetchone()

            if existing_item:
                return False, "An item with this code already exists"

            self.cursor.execute('''
            UPDATE items 
            SET code = ?, name = ?, category = ?, location = ?, description = ?
            WHERE id = ?
            ''', (code, name, category, location, description, item_id))
            self.conn.commit()
            return True, "Item updated successfully"
        except sqlite3.Error as e:
            print(f"Error updating item: {e}")
            return False, f"Database error: {e}"

    def delete_item(self, item_id):
        """Delete an item from the inventory"""
        try:
            # Check if the item is currently borrowed
            self.cursor.execute('''
            SELECT COUNT(*) FROM borrowings 
            WHERE item_id = ? AND return_date IS NULL
            ''', (item_id,))

            if self.cursor.fetchone()[0] > 0:
                return False, "Cannot delete item that is currently borrowed"

            self.cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
            self.conn.commit()
            return True, "Item deleted successfully"
        except sqlite3.Error as e:
            print(f"Error deleting item: {e}")
            return False, f"Database error: {e}"

    def get_item_by_id(self, item_id):
        """Get an item by its ID"""
        try:
            self.cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting item: {e}")
            return None

    def get_borrowing_history(self, limit=100):
        """Get the borrowing history"""
        try:
            self.cursor.execute('''
            SELECT b.id, u.username, i.code, i.name, b.borrow_date, b.return_date
            FROM borrowings b
            JOIN users u ON b.user_id = u.id
            JOIN items i ON b.item_id = i.id
            ORDER BY b.borrow_date DESC
            LIMIT ?
            ''', (limit,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting borrowing history: {e}")
            return []

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            print("Database connection closed")

    def __del__(self):
        """Destructor to ensure connection is closed when object is garbage collected"""
        self.close()
