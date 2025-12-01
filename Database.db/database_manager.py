import sqlite3
import pandas as pd
from typing import List, Tuple, Optional, Any, Dict

class DatabaseManager:
    """
    A class to manage SQLite database operations for the Multi-Domain Intelligence Platform.
    Handles connection, cursor operations, and provides safe CRUD functionality.
    """
    
    def __init__(self, db_name: str = "intelligence_platform.db"):
        """
        Initialize the DatabaseManager with a connection to the SQLite database.
        
        Args:
            db_name (str): The name of the SQLite database file
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self) -> None:
        """Establish connection to the SQLite database and create cursor."""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Successfully connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise  # Re-raise the exception to handle it at higher level
    
    def execute_query(self, query: str, params: Tuple = ()) -> Optional[List[Tuple]]:
        """
        Execute a SQL query safely using parameterized queries to prevent SQL injection.
        
        Args:
            query (str): The SQL query to execute
            params (Tuple): Parameters for the query
            
        Returns:
            Optional[List[Tuple]]: Query results if it's a SELECT query, None otherwise
        """
        try:
            self.cursor.execute(query, params)
            
            # If it's a SELECT query, return results
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                # For INSERT, UPDATE, DELETE - commit the changes
                self.connection.commit()
                return None
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            print(f"Failed query: {query}")
            if self.connection:
                self.connection.rollback()  # Rollback on error
            return None
    
    def create_tables(self) -> bool:
        """
        Create all necessary tables for the platform if they don't exist.
        
        Returns:
            bool: True if tables created successfully, False otherwise
        """
        # Users table for authentication
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # Cybersecurity incidents table
        cyber_incidents_table = """
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            severity TEXT CHECK(severity IN ('Low', 'Medium', 'High', 'Critical')),
            status TEXT CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
            category TEXT,
            assigned_to TEXT,
            date_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_resolved TIMESTAMP,
            resolution_time_hours REAL
        );
        """
        
        # Data science datasets metadata table
        datasets_metadata_table = """
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            source_department TEXT,
            file_size_mb REAL,
            row_count INTEGER,
            column_count INTEGER,
            data_quality_score REAL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_accessed TIMESTAMP,
            is_archived BOOLEAN DEFAULT 0
        );
        """
        
        # IT operations tickets table
        it_tickets_table = """
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            assignee TEXT,
            reporter TEXT,
            status TEXT CHECK(status IN ('New', 'Assigned', 'In Progress', 'Waiting for User', 'Resolved', 'Closed')),
            priority TEXT CHECK(priority IN ('Low', 'Medium', 'High', 'Urgent')),
            category TEXT,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_assigned TIMESTAMP,
            date_resolved TIMESTAMP,
            resolution_notes TEXT
        );
        """
        
        tables = [
            users_table,
            cyber_incidents_table, 
            datasets_metadata_table,
            it_tickets_table
        ]
        
        success = True
        for table_query in tables:
            result = self.execute_query(table_query)
            if result is None:  # Check if query executed successfully
                continue
            else:
                success = False
        
        if success:
            print("All tables created successfully!")
        else:
            print("Some tables may already exist.")
        
        return success
    
    def get_user_by_username(self, username: str) -> Optional[Tuple]:
        """
        Retrieve a user by their username.
        
        Args:
            username (str): The username to search for
            
        Returns:
            Optional[Tuple]: The user record if found, None otherwise
        """
        query = "SELECT * FROM users WHERE username = ?"
        result = self.execute_query(query, (username,))
        return result[0] if result else None
    
    def migrate_users_from_file(self, file_path: str = "users.txt") -> bool:
        """
        Migrate user data from text file to SQLite database.
        
        Args:
            file_path (str): Path to the users.txt file
            
        Returns:
            bool: True if migration successful, False otherwise
        """
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            migrated_count = 0
            for line in lines:
                if line.strip():
                    # Assuming format: username,password_hash,role
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        username, password_hash, role = parts[0], parts[1], parts[2]
                        
                        # Check if user already exists
                        existing_user = self.get_user_by_username(username)
                        
                        if not existing_user:
                            self.execute_query(
                                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                                (username, password_hash, role)
                            )
                            migrated_count += 1
            
            print(f"Successfully migrated {migrated_count} users to database.")
            return True
            
        except FileNotFoundError:
            print(f"Users file {file_path} not found.")
            return False
        except Exception as e:
            print(f"Error during user migration: {e}")
            return False
    
    def load_csv_data(self, csv_file_path: str, table_name: str) -> bool:
        """
        Load data from CSV file into specified table using pandas.
        
        Args:
            csv_file_path (str): Path to the CSV file
            table_name (str): Name of the target table
            
        Returns:
            bool: True if loading successful, False otherwise
        """
        try:
            # Read CSV file
            df = pd.read_csv(csv_file_path)
            
            # Load data into SQLite table
            df.to_sql(table_name, self.connection, if_exists='append', index=False)
            self.connection.commit()
            
            print(f"Successfully loaded data from {csv_file_path} into {table_name} table.")
            return True
            
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def get_all_records(self, table_name: str) -> List[Tuple]:
        """
        Retrieve all records from a specified table.
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            List[Tuple]: All records from the table
        """
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query) or []
    
    def insert_record(self, table_name: str, data: dict) -> bool:
        """
        Insert a new record into the specified table.
        
        Args:
            table_name (str): Name of the table
            data (dict): Column-value pairs for the new record
            
        Returns:
            bool: True if insertion successful, False otherwise
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        result = self.execute_query(query, values)
        return result is None  # execute_query returns None for successful INSERT
    
    def update_record(self, table_name: str, record_id: int, data: dict) -> bool:
        """
        Update an existing record in the specified table.
        
        Args:
            table_name (str): Name of the table
            record_id (int): ID of the record to update
            data (dict): Column-value pairs to update
            
        Returns:
            bool: True if update successful, False otherwise
        """
        if not data:
            print("No data provided for update")
            return False
            
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values()) + (record_id,)
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
        
        result = self.execute_query(query, values)
        return result is None  # execute_query returns None for successful UPDATE
    
    def delete_record(self, table_name: str, record_id: int) -> bool:
        """
        Delete a record from the specified table.
        
        Args:
            table_name (str): Name of the table
            record_id (int): ID of the record to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        query = f"DELETE FROM {table_name} WHERE id = ?"
        
        result = self.execute_query(query, (record_id,))
        return result is None  # execute_query returns None for successful DELETE
    
    def get_record_by_id(self, table_name: str, record_id: int) -> Optional[Tuple]:
        """
        Retrieve a specific record by ID.
        
        Args:
            table_name (str): Name of the table
            record_id (int): ID of the record to retrieve
            
        Returns:
            Optional[Tuple]: The record if found, None otherwise
        """
        query = f"SELECT * FROM {table_name} WHERE id = ?"
        result = self.execute_query(query, (record_id,))
        return result[0] if result else None
    
    def get_cyber_incidents(self, filters: Dict = None) -> List[Tuple]:
        """
        Retrieve cyber incidents with optional filtering.
        
        Args:
            filters (dict): Optional filters like {'status': 'Open', 'severity': 'High'}
            
        Returns:
            List[Tuple]: Cyber incident records
        """
        base_query = "SELECT * FROM cyber_incidents"
        params = []
        
        if filters:
            where_clauses = []
            for key, value in filters.items():
                where_clauses.append(f"{key} = ?")
                params.append(value)
            
            if where_clauses:
                base_query += " WHERE " + " AND ".join(where_clauses)
        
        base_query += " ORDER BY date_reported DESC"
        return self.execute_query(base_query, tuple(params)) or []
    
    def get_datasets(self, filters: Dict = None) -> List[Tuple]:
        """
        Retrieve datasets with optional filtering.
        
        Args:
            filters (dict): Optional filters like {'source_department': 'Sales', 'is_archived': 0}
            
        Returns:
            List[Tuple]: Dataset records
        """
        base_query = "SELECT * FROM datasets_metadata"
        params = []
        
        if filters:
            where_clauses = []
            for key, value in filters.items():
                where_clauses.append(f"{key} = ?")
                params.append(value)
            
            if where_clauses:
                base_query += " WHERE " + " AND ".join(where_clauses)
        
        base_query += " ORDER BY upload_date DESC"
        return self.execute_query(base_query, tuple(params)) or []
    
    def get_it_tickets(self, filters: Dict = None) -> List[Tuple]:
        """
        Retrieve IT tickets with optional filtering.
        
        Args:
            filters (dict): Optional filters like {'status': 'Open', 'priority': 'High'}
            
        Returns:
            List[Tuple]: IT ticket records
        """
        base_query = "SELECT * FROM it_tickets"
        params = []
        
        if filters:
            where_clauses = []
            for key, value in filters.items():
                where_clauses.append(f"{key} = ?")
                params.append(value)
            
            if where_clauses:
                base_query += " WHERE " + " AND ".join(where_clauses)
        
        base_query += " ORDER BY date_created DESC"
        return self.execute_query(base_query, tuple(params)) or []
    
    def create_demo_users(self) -> int:
        """
        Create demo users for testing if they don't exist.
        
        Returns:
            int: Number of demo users created
        """
        import bcrypt
        
        demo_users = [
            ('john_analyst', 'password123', 'cyber_analyst'),
            ('sara_scientist', 'password123', 'data_scientist'),
            ('mike_admin', 'password123', 'it_administrator'),
            ('Joel_analyst', 'password123', 'cyber_analyst'),
            ('Sara_scientist', 'password123', 'data_scientist'),
            ('Daniel_admin', 'password123', 'it_administrator')
        ]
        
        created_count = 0
        for username, password, role in demo_users:
            # Check if user already exists
            existing_user = self.get_user_by_username(username)
            
            if not existing_user:
                try:
                    # Hash password
                    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    # Insert user
                    self.execute_query(
                        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, hashed_pw, role)
                    )
                    created_count += 1
                    print(f"Created demo user: {username}")
                    
                except Exception as e:
                    # If bcrypt fails, use pre-hashed password for 'password123'
                    pre_hashed = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'
                    self.execute_query(
                        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                        (username, pre_hashed, role)
                    )
                    created_count += 1
                    print(f"Created demo user with pre-hashed password: {username}")
        
        return created_count
    
    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
    
    def __enter__(self):
        """Support context manager protocol."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support context manager protocol."""
        self.close()


# Example usage and testing
if __name__ == "__main__":
    # Create database manager instance
    db = DatabaseManager()
    
    # Create all tables
    db.create_tables()
    
    # Create demo users
    demo_users_created = db.create_demo_users()
    print(f"Created {demo_users_created} demo users")
    
    # Example: Migrate users from text file (run this after Week 7)
    # db.migrate_users_from_file("users.txt")
    
    # Example: Load sample data from CSV files
    # db.load_csv_data("cyber_incidents.csv", "cyber_incidents")
    # db.load_csv_data("datasets_metadata.csv", "datasets_metadata") 
    # db.load_csv_data("it_tickets.csv", "it_tickets")
    
    # Example CRUD operations
    print("\n--- Testing CRUD Operations ---")
    
    # Create (Insert) a new cyber incident
    new_incident = {
        'title': 'Test Phishing Attempt',
        'description': 'Suspicious email detected',
        'severity': 'High',
        'status': 'Open',
        'category': 'Phishing'
    }
    if db.insert_record('cyber_incidents', new_incident):
        print("✓ New incident created successfully")
    
    # Read all incidents
    incidents = db.get_all_records('cyber_incidents')
    print(f"✓ Retrieved {len(incidents)} incidents")
    
    # Update an incident (assuming we have at least one record)
    if incidents:
        incident_id = incidents[0][0]  # Get first incident's ID
        update_data = {'status': 'In Progress', 'assigned_to': 'Analyst_1'}
        if db.update_record('cyber_incidents', incident_id, update_data):
            print("✓ Incident updated successfully")
    
    # Delete the test incident
    if incidents:  # Only delete if we have incidents
        if db.delete_record('cyber_incidents', incident_id):
            print("✓ Test incident deleted successfully")
    
    # Test filtered queries
    print("\n--- Testing Filtered Queries ---")
    filtered_incidents = db.get_cyber_incidents({'status': 'Open'})
    print(f"✓ Retrieved {len(filtered_incidents)} incidents with status 'Open'")
    
    # Test get_user_by_username
    print("\n--- Testing User Retrieval ---")
    test_user = db.get_user_by_username('john_analyst')
    if test_user:
        print(f"✓ Found user: {test_user[1]} (Role: {test_user[3]})")
    else:
        print("✗ User not found")
    
    # Close connection
    db.close()