
def create_cyber_incident(self, incident_data: dict) -> bool:
    """Create a new cyber incident."""
    required_fields = ['title', 'severity', 'status', 'category']
    
    for field in required_fields:
        if field not in incident_data:
            print(f"Missing required field: {field}")
            return False
    
    return self.insert_record('cyber_incidents', incident_data)

def update_cyber_incident(self, incident_id: int, update_data: dict) -> bool:
    """Update an existing cyber incident."""
    return self.update_record('cyber_incidents', incident_id, update_data)

def delete_cyber_incident(self, incident_id: int) -> bool:
    """Delete a cyber incident."""
    return self.delete_record('cyber_incidents', incident_id)

# Data Science Domain CRUD
def get_datasets(self, filters: dict = None) -> List[Tuple]:
    """Retrieve datasets with optional filtering."""
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

def create_dataset(self, dataset_data: dict) -> bool:
    """Create a new dataset entry."""
    required_fields = ['name', 'source_department', 'file_size_mb']
    
    for field in required_fields:
        if field not in dataset_data:
            print(f"Missing required field: {field}")
            return False
    
    return self.insert_record('datasets_metadata', dataset_data)

def update_dataset(self, dataset_id: int, update_data: dict) -> bool:
    """Update an existing dataset."""
    return self.update_record('datasets_metadata', dataset_id, update_data)

def delete_dataset(self, dataset_id: int) -> bool:
    """Delete a dataset."""
    return self.delete_record('datasets_metadata', dataset_id)

# IT Operations Domain CRUD
def get_it_tickets(self, filters: dict = None) -> List[Tuple]:
    """Retrieve IT tickets with optional filtering."""
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

def create_it_ticket(self, ticket_data: dict) -> bool:
    """Create a new IT ticket."""
    required_fields = ['title', 'status', 'priority', 'category']
    
    for field in required_fields:
        if field not in ticket_data:
            print(f"Missing required field: {field}")
            return False
    
    return self.insert_record('it_tickets', ticket_data)

def update_it_ticket(self, ticket_id: int, update_data: dict) -> bool:
    """Update an existing IT ticket."""
    return self.update_record('it_tickets', ticket_id, update_data)

def delete_it_ticket(self, ticket_id: int) -> bool:
    """Delete an IT ticket."""
    return self.delete_record('it_tickets', ticket_id)

# User Management CRUD
def get_user_by_username(self, username: str) -> Optional[Tuple]:
    """Get user by username for authentication."""
    query = "SELECT * FROM users WHERE username = ?"
    result = self.execute_query(query, (username,))
    return result[0] if result else None

def create_user(self, user_data: dict) -> bool:
    """Create a new user."""
    required_fields = ['username', 'password_hash', 'role']
    
    for field in required_fields:
        if field not in user_data:
            print(f"Missing required field: {field}")
            return False
    
    return self.insert_record('users', user_data)