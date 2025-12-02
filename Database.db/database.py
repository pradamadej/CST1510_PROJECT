import sqlite3
import pandas as pd
from typing import List, Tuple, Optional, Any, Dict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            # Enable foreign keys
            self.cursor.execute("PRAGMA foreign_keys = ON")
            logger.info(f"Successfully connected to database: {self.db_name}")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
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
            logger.error(f"Database error: {e}")
            logger.error(f"Failed query: {query}")
            self.connection.rollback()  # Rollback on error
            return None
    
    def execute_many(self, query: str, params_list: List[Tuple]) -> bool:
        """
        Execute multiple SQL statements efficiently.
        
        Args:
            query (str): The SQL query to execute
            params_list (List[Tuple]): List of parameter tuples
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cursor.executemany(query, params_list)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Database error in executemany: {e}")
            self.connection.rollback()
            return False
    
    def create_tables(self) -> None:
        """Create all necessary tables for the platform if they don't exist."""
        
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
        
        # User activity log table
        user_activity_table = """
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            activity_type TEXT,
            description TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """
        
        tables = [
            users_table,
            cyber_incidents_table, 
            datasets_metadata_table,
            it_tickets_table,
            user_activity_table
        ]
        
        for table_query in tables:
            try:
                self.execute_query(table_query)
            except Exception as e:
                logger.error(f"Error creating table: {e}")
                continue
        
        logger.info("All tables created/verified successfully!")
    
    def migrate_users_from_file(self, file_path: str = "users.txt") -> int:
        """
        Migrate user data from text file to SQLite database.
        
        Args:
            file_path (str): Path to the users.txt file
            
        Returns:
            int: Number of users migrated successfully
        """
        migrated_count = 0
        
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Assuming format: username,password_hash,role
                parts = [part.strip() for part in line.split(',')]
                if len(parts) >= 3:
                    username, password_hash, role = parts[0], parts[1], parts[2]
                    
                    # Check if user already exists
                    existing_user = self.execute_query(
                        "SELECT id FROM users WHERE username = ?", 
                        (username,)
                    )
                    
                    if not existing_user:
                        success = self.insert_record('users', {
                            'username': username,
                            'password_hash': password_hash,
                            'role': role
                        })
                        if success:
                            migrated_count += 1
            
            logger.info(f"Successfully migrated {migrated_count} users to database.")
            return migrated_count
            
        except FileNotFoundError:
            logger.warning(f"Users file {file_path} not found.")
            return 0
        except Exception as e:
            logger.error(f"Error during user migration: {e}")
            return 0
    
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
            
            # Convert column names to lowercase for consistency
            df.columns = [col.lower() for col in df.columns]
            
            # Load data into SQLite table
            df.to_sql(table_name, self.connection, if_exists='append', index=False)
            
            logger.info(f"Successfully loaded data from {csv_file_path} into {table_name} table.")
            return True
            
        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_file_path}")
            return False
        except Exception as e:
            logger.error(f"Error loading CSV data: {e}")
            return False
    
    def get_all_records(self, table_name: str) -> List[Tuple]:
        """
        Retrieve all records from a specified table.
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            List[Tuple]: All records from the table
        """
        # Sanitize table name to prevent SQL injection
        if not table_name.replace('_', '').isalnum():
            logger.error(f"Invalid table name: {table_name}")
            return []
        
        query = f"SELECT * FROM {table_name}"
        result = self.execute_query(query)
        return result or []
    
    def get_records_with_limit(self, table_name: str, limit: int = 100, offset: int = 0) -> List[Tuple]:
        """
        Retrieve records with pagination.
        
        Args:
            table_name (str): Name of the table
            limit (int): Maximum number of records to return
            offset (int): Number of records to skip
            
        Returns:
            List[Tuple]: Records from the table
        """
        # Sanitize table name
        if not table_name.replace('_', '').isalnum():
            logger.error(f"Invalid table name: {table_name}")
            return []
        
        query = f"SELECT * FROM {table_name} LIMIT ? OFFSET ?"
        result = self.execute_query(query, (limit, offset))
        return result or []
    
    def insert_record(self, table_name: str, data: dict) -> bool:
        """
        Insert a new record into the specified table.
        
        Args:
            table_name (str): Name of the table
            data (dict): Column-value pairs for the new record
            
        Returns:
            bool: True if insertion successful, False otherwise
        """
        if not data:
            logger.warning("No data provided for insertion")
            return False
        
        # Sanitize table name
        if not table_name.replace('_', '').isalnum():
            logger.error(f"Invalid table name: {table_name}")
            return False
        
        # Filter out None values
        data = {k: v for k, v in data.items() if v is not None}
        
        if not data:
            logger.warning("Only None values provided for insertion")
            return False
        
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
            logger.warning("No data provided for update")
            return False
        
        # Sanitize table name
        if not table_name.replace('_', '').isalnum():
            logger.error(f"Invalid table name: {table_name}")
            return False
        
        # Filter out None values
        data = {k: v for k, v in data.items() if v is not None}
        
        if not data:
            logger.warning("Only None values provided for update")
            return False
        
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values()) + (record_id,)
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
        
        result = self.execute_query(query, values)
        return result is None
    
    def delete_record(self, table_name: str, record_id: int) -> bool:
        """
        Delete a record from the specified table.
        
        Args:
            table_name (str): Name of the table
            record_id (int): ID of the record to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        # Sanitize table name
        if not table_name.replace('_', '').isalnum():
            logger.error(f"Invalid table name: {table_name}")
            return False
        
        query = f"DELETE FROM {table_name} WHERE id = ?"
        
        result = self.execute_query(query, (record_id,))
        return result is None
    
    def get_record_by_id(self, table_name: str, record_id: int) -> Optional[Tuple]:
        """
        Retrieve a specific record by ID.
        
        Args:
            table_name (str): Name of the table
            record_id (int): ID of the record to retrieve
            
        Returns:
            Optional[Tuple]: The record if found, None otherwise
        """
        # Sanitize table name
        if not table_name.replace('_', '').isalnum():
            logger.error(f"Invalid table name: {table_name}")
            return None
        
        query = f"SELECT * FROM {table_name} WHERE id = ?"
        result = self.execute_query(query, (record_id,))
        return result[0] if result else None
    
    def search_records(self, table_name: str, search_column: str, search_value: str) -> List[Tuple]:
        """
        Search for records where a column contains a value.
        
        Args:
            table_name (str): Name of the table
            search_column (str): Column to search in
            search_value (str): Value to search for
            
        Returns:
            List[Tuple]: Matching records
        """
        # Sanitize inputs
        if not table_name.replace('_', '').isalnum():
            logger.error(f"Invalid table name: {table_name}")
            return []
        
        if not search_column.replace('_', '').isalnum():
            logger.error(f"Invalid column name: {search_column}")
            return []
        
        query = f"SELECT * FROM {table_name} WHERE {search_column} LIKE ?"
        result = self.execute_query(query, (f'%{search_value}%',))
        return result or []
    
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
                if key.replace('_', '').isalnum():  # Sanitize column name
                    where_clauses.append(f"{key} = ?")
                    params.append(value)
            
            if where_clauses:
                base_query += " WHERE " + " AND ".join(where_clauses)
        
        base_query += " ORDER BY date_reported DESC"
        return self.execute_query(base_query, tuple(params)) or []
    
    def get_table_columns(self, table_name: str) -> List[str]:
        """
        Get column names for a table.
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            List[str]: Column names
        """
        # Sanitize table name
        if not table_name.replace('_', '').isalnum():
            logger.error(f"Invalid table name: {table_name}")
            return []
        
        query = f"PRAGMA table_info({table_name})"
        result = self.execute_query(query)
        return [column[1] for column in result] if result else []
    
    def record_exists(self, table_name: str, column: str, value: Any) -> bool:
        """
        Check if a record exists in a table.
        
        Args:
            table_name (str): Name of the table
            column (str): Column to check
            value (Any): Value to look for
            
        Returns:
            bool: True if record exists, False otherwise
        """
        # Sanitize inputs
        if not table_name.replace('_', '').isalnum():
            logger.error(f"Invalid table name: {table_name}")
            return False
        
        if not column.replace('_', '').isalnum():
            logger.error(f"Invalid column name: {column}")
            return False
        
        query = f"SELECT 1 FROM {table_name} WHERE {column} = ? LIMIT 1"
        result = self.execute_query(query, (value,))
        return bool(result)
    
    def get_user_by_username(self, username: str) -> Optional[Tuple]:
        """
        Get user by username.
        
        Args:
            username (str): Username to search for
            
        Returns:
            Optional[Tuple]: User record if found, None otherwise
        """
        query = "SELECT * FROM users WHERE username = ?"
        result = self.execute_query(query, (username,))
        return result[0] if result else None
    
    def log_user_activity(self, user_id: Optional[int], username: str, activity_type: str, description: str) -> bool:
        """
        Log user activity.
        
        Args:
            user_id (Optional[int]): User ID (can be None)
            username (str): Username
            activity_type (str): Type of activity
            description (str): Activity description
            
        Returns:
            bool: True if logged successfully
        """
        return self.insert_record('user_activity', {
            'user_id': user_id,
            'username': username,
            'activity_type': activity_type,
            'description': description
        })
    
    def get_database_stats(self) -> Dict[str, int]:
        """
        Get statistics about the database.
        
        Returns:
            Dict[str, int]: Table name -> row count
        """
        stats = {}
        tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets', 'user_activity']
        
        for table in tables:
            query = f"SELECT COUNT(*) FROM {table}"
            result = self.execute_query(query)
            if result:
                stats[table] = result[0][0]
        
        return stats
    
    def backup_database(self, backup_path: str) -> bool:
        """
        Create a backup of the database.
        
        Args:
            backup_path (str): Path to save the backup
            
        Returns:
            bool: True if backup successful
        """
        try:
            backup_conn = sqlite3.connect(backup_path)
            with backup_conn:
                self.connection.backup(backup_conn)
            backup_conn.close()
            logger.info(f"Database backup created at {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating database backup: {e}")
            return False
    
    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed.")
    
    def __enter__(self):
        """Support context manager protocol."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support context manager protocol."""
        self.close()


# Example usage and testing
if __name__ == "__main__":
    # Create database manager instance
    db = DatabaseManager("test_platform.db")
    
    # Create all tables
    db.create_tables()
    
    # Insert sample users
    sample_users = [
        {
            'username': 'john_analyst',
            'password_hash': 'hashed_password_123',
            'role': 'analyst'
        },
        {
            'username': 'sara_scientist',
            'password_hash': 'hashed_password_456',
            'role': 'scientist'
        },
        {
            'username': 'mike_admin',
            'password_hash': 'hashed_password_789',
            'role': 'admin'
        }
    ]
    
    for user in sample_users:
        db.insert_record('users', user)
    
    # Insert sample cyber incidents
    sample_incidents = [
        {
            'title': 'Phishing Attempt Detected',
            'description': 'Multiple phishing emails targeting employees',
            'severity': 'High',
            'status': 'Open',
            'category': 'Phishing'
        },
        {
            'title': 'Unauthorized Access',
            'description': 'Suspicious login attempts from unknown IP',
            'severity': 'Critical',
            'status': 'In Progress',
            'category': 'Access Control'
        }
    ]
    
    for incident in sample_incidents:
        db.insert_record('cyber_incidents', incident)
    
    # Test CRUD operations
    print("\n--- Testing CRUD Operations ---")
    
    # Create (Insert) a new cyber incident
    new_incident = {
        'title': 'Test Security Alert',
        'description': 'Test incident for verification',
        'severity': 'Medium',
        'status': 'Open',
        'category': 'Testing'
    }
    
    if db.insert_record('cyber_incidents', new_incident):
        print("✓ New incident created successfully")
    
    # Read all incidents
    incidents = db.get_all_records('cyber_incidents')
    print(f"✓ Retrieved {len(incidents)} incidents")
    
    # Update an incident
    if incidents:
        incident_id = incidents[0][0]
        update_data = {'status': 'In Progress', 'assigned_to': 'Analyst_1'}
        if db.update_record('cyber_incidents', incident_id, update_data):
            print("✓ Incident updated successfully")
    
    # Test filtered query
    print("\n--- Testing Filtered Query ---")
    filtered_incidents = db.get_cyber_incidents({'status': 'Open'})
    print(f"✓ Retrieved {len(filtered_incidents)} incidents with status 'Open'")
    
    # Test search
    print("\n--- Testing Search ---")
    search_results = db.search_records('cyber_incidents', 'title', 'phishing')
    print(f"✓ Found {len(search_results)} incidents with 'phishing' in title")
    
    # Get database stats
    print("\n--- Database Statistics ---")
    stats = db.get_database_stats()
    for table, count in stats.items():
        print(f"  {table}: {count} records")
    
    # Test user activity logging
    print("\n--- Testing User Activity Logging ---")
    db.log_user_activity(1, 'john_analyst', 'LOGIN', 'User logged into the system')
    db.log_user_activity(1, 'john_analyst', 'SEARCH', 'User searched for incidents')
    
    # Test user lookup
    user = db.get_user_by_username('john_analyst')
    if user:
        print(f"✓ Found user: {user[1]} (Role: {user[3]})")
    
    # Close connection
    db.close()
    
    # Clean up test database
    import os
    if os.path.exists("test_platform.db"):
        os.remove("test_platform.db")
        print("\n✓ Cleaned up test database")