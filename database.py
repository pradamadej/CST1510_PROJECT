Import sqlite3

# Connect to database 
conn = sqlite3.connect('DATA/intelligence_platform.db’) 
cursor = conn.cursor()
 
# Create table 
cursor.execute(""" CREATE TABLE IF NOT EXISTS users ( 
id INTEGER PRIMARY KEY AUTOINCREMENT, 
username TEXT NOT NULL UNIQUE, 
password_hash TEXT NOT NULL, 
role TEXT DEFAULT 'user' ) """) 

# Commit changes
conn.commit()

# Inserting a user securely using parameterized query
conn = sqlite3.connect('DATA/intelligence_platform.db’) 
cursor = conn.cursor()
cursor.execute(""" INSERT INTO users 
(username, password_hash, role) VALUES (?, ?, ?) """, ('alice', 'hashed_password_123', 'admin’)) # ALWAYS use ? placeholders 
conn.commit() 

# Querying users
cursor.execute("SELECT * FROM users") 
all_users = cursor.fetchall() # Returns list of all rows

cursor.execute( "SELECT * FROM users WHERE username = ?", ('alice',) ) 
user = cursor.fetchone() # Returns single row or None

cursor.execute( "SELECT username, role FROM users WHERE role = ?", ('admin',) ) 
admins = cursor.fetchall() # Returns list of matching rows

# Updating a user's role securely
cursor.execute(""" UPDATE users SET role = ? WHERE username = ? """, ('admin', 'alice’))
 conn.commit()
 # Verify the update 
cursor.execute(""" SELECT username, role FROM users WHERE username = ? """, ('alice',)) 
result = cursor.fetchone() 
print(f"Updated: {result}")

# Deleting a user securely
cursor.execute(""" DELETE FROM users WHERE username = ? """, ('alice',)) 
conn.commit() 
# Verify deletion
print(f"Deleted {cursor.rowcount} user(s)")

# Loading data from CSV files into the database
Import pandas as pd
Importsqlite3
# Read CSV into DataFrame 
df = pd.read_csv('DATA/cyber_incidents.csv')
# View first 5 rowsprint(df.head()) # Check data types and missing valuesprint(df.info()) # Check for missing dataprint(df.isnull().sum())
# Connect to database
 conn = sqlite3.connect('DATA/intelligence_platform.db’)
 # Bulk insert all rows 
df.to_sql( 'cyber_incidents', conn, if_exists='append', index=False ) 
print("✓ Data loaded successfully")
# Count rows in database 
cursor = conn.cursor() 
cursor.execute("SELECT COUNT(*) FROM cyber_incidents") count = cursor.fetchone()[0] 
print(f"Loaded {count} incidents") # View sample data cursor.execute("SELECT * FROM cyber_incidents LIMIT 3") 
for row in cursor.fetchall(): 
                print(row)



