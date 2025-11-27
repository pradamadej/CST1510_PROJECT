import sqlite3
import os
from database import DatabaseManager  # Import the class we created

def migrate_users_from_file(db_manager, file_path="users.txt"):
    """
    Migrate user data from text file to SQLite database users table.
    
    Args:
        db_manager: Instance of DatabaseManager
        file_path (str): Path to the users.txt file
        
    Returns:
        tuple: (success_count, error_count, total_users)
    """
    # Check if the users file exists
    if not os.path.exists(file_path):
        print(f"❌ Error: Users file '{file_path}' not found.")
        print("Please make sure you have completed Week 7 and the users.txt file exists.")
        return 0, 0, 0
    
    success_count = 0
    error_count = 0
    total_users = 0
    
    print(f"📁 Reading users from: {file_path}")
    print("-" * 50)
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        for line_num, line in enumerate(lines, 1):
            if line.strip():  # Skip empty lines
                total_users += 1
                
                # Remove any extra whitespace and split by comma
                clean_line = line.strip()
                parts = clean_line.split(',')
                
                # Validate the line format
                if len(parts) >= 3:
                    username = parts[0].strip()
                    password_hash = parts[1].strip()
                    role = parts[2].strip()
                    
                    print(f"👤 Processing user {line_num}: {username} ({role})")
                    
                    # Check if user already exists in database
                    existing_user = db_manager.execute_query(
                        "SELECT id FROM users WHERE username = ?", 
                        (username,)
                    )
                    
                    if existing_user:
                        print(f"   ⚠️  User '{username}' already exists in database. Skipping.")
                        error_count += 1
                    else:
                        # Insert new user into database
                        result = db_manager.execute_query(
                            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                            (username, password_hash, role)
                        )
                        
                        if result is None:  # Successful insertion
                            print(f"   ✅ Successfully added user '{username}'")
                            success_count += 1
                        else:
                            print(f"   ❌ Failed to add user '{username}'")
                            error_count += 1
                
                else:
                    print(f"❌ Invalid format in line {line_num}: {clean_line}")
                    print("   Expected format: username,password_hash,role")
                    error_count += 1
        
        print("-" * 50)
        print("📊 Migration Summary:")
        print(f"   Total users in file: {total_users}")
        print(f"   ✅ Successfully migrated: {success_count}")
        print(f"   ❌ Errors/Skipped: {error_count}")
        
        return success_count, error_count, total_users
        
    except Exception as e:
        print(f"❌ Unexpected error during migration: {e}")
        return success_count, error_count, total_users

def display_current_users(db_manager):
    """Display all users currently in the database."""
    print("\n👥 Current users in database:")
    print("-" * 50)
    
    users = db_manager.get_all_records('users')
    
    if not users:
        print("   No users found in database.")
    else:
        for user in users:
            user_id, username, password_hash, role, created_at = user
            print(f"   ID: {user_id}, Username: {username}, Role: {role}")
            print(f"      Hash: {password_hash[:20]}...")  # Show first 20 chars of hash
            print(f"      Created: {created_at}")
            print()

def create_sample_users_file():
    """Create a sample users.txt file if it doesn't exist (for testing)."""
    sample_users = [
        "john_analyst,$2b$12$abc123...hash1,cyber_analyst",
        "sara_scientist,$2b$12$def456...hash2,data_scientist", 
        "mike_admin,$2b$12$ghi789...hash3,it_administrator",
        "test_user,$2b$12$jkl012...hash4,cyber_analyst"
    ]
    
    with open("users.txt", "w") as f:
        for user_line in sample_users:
            f.write(user_line + "\n")
    
    print("📝 Created sample users.txt file for testing.")

def main():
    """Main function to run the user migration."""
    print("🚀 Starting User Migration from users.txt to SQLite Database")
    print("=" * 60)
    
    # Check if users.txt exists, if not offer to create a sample
    if not os.path.exists("users.txt"):
        print("❌ users.txt file not found.")
        create_sample = input("   Would you like to create a sample users.txt file for testing? (y/n): ")
        if create_sample.lower() == 'y':
            create_sample_users_file()
        else:
            print("Please complete Week 7 first to create your users.txt file.")
            return
    
    # Initialize database manager
    try:
        db = DatabaseManager()
        
        # Ensure users table exists
        db.create_tables()
        print("✅ Database connection established and tables verified.")
        
        # Perform migration
        success_count, error_count, total_users = migrate_users_from_file(db)
        
        # Display current state of users table
        display_current_users(db)
        
        # Summary
        print("\n🎯 Migration Complete!")
        if success_count == total_users:
            print("✅ All users migrated successfully!")
        elif success_count > 0:
            print(f"⚠️  {success_count}/{total_users} users migrated successfully.")
        else:
            print("❌ No users were migrated. Please check your users.txt file format.")
        
        # Close database connection
        db.close()
        
    except Exception as e:
        print(f"❌ Database error: {e}")

# Alternative version using direct SQLite connection (if you prefer)
def migrate_users_direct():
    """
    Alternative migration function using direct SQLite connection
    instead of the DatabaseManager class.
    """
    print("\n🔄 Alternative: Using direct SQLite connection")
    
    if not os.path.exists("users.txt"):
        print("❌ users.txt file not found.")
        return
    
    try:
        # Connect directly to SQLite
        conn = sqlite3.connect("intelligence_platform.db")
        cursor = conn.cursor()
        
        # Ensure users table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        with open("users.txt", 'r') as file:
            lines = file.readlines()
        
        migrated_count = 0
        for line in lines:
            if line.strip():
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    username, password_hash, role = parts[0], parts[1], parts[2]
                    
                    try:
                        cursor.execute(
                            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                            (username, password_hash, role)
                        )
                        migrated_count += 1
                        print(f"✅ Migrated: {username}")
                    except sqlite3.IntegrityError:
                        print(f"⚠️  Skipped (already exists): {username}")
        
        conn.commit()
        conn.close()
        print(f"📊 Direct migration complete: {migrated_count} users migrated.")
        
    except Exception as e:
        print(f"❌ Error in direct migration: {e}")

if __name__ == "__main__":
    # Run the main migration
    main()
    
    # Uncomment the line below if you want to try the direct migration method
    # migrate_users_direct()
    
    print("\n✅ Migration script finished!")
    print("\n📝 Next steps:")
    print("   1. Check the output above for any errors")
    print("   2. Your users are now in the SQLite database")
    print("   3. You can now use the database for login in")