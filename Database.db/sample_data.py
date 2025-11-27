# Load sample data for testing

from database import DatabaseManager
import os

def create_sample_csv_files():
    """Create sample CSV files if they don't exist."""
    
    # Sample cyber incidents CSV
    cyber_csv_content = """title,description,severity,status,category,assigned_to,date_reported
Phishing Email Campaign,Targeted phishing emails sent to employees,High,Open,Phishing,john_analyst,2024-01-15 09:30:00
Ransomware Detection,Ransomware on file server,Critical,In Progress,Malware,sarah_security,2024-01-14 14:20:00
Unauthorized Access,Multiple failed login attempts,Medium,Resolved,Unauthorized Access,mike_admin,2024-01-13 11:15:00
Data Exfiltration,Large data transfer to external server,High,Open,Data Loss,john_analyst,2024-01-15 10:45:00
DDoS Attack,Denial of service on web servers,Critical,In Progress,Network Attack,sarah_security,2024-01-14 16:30:00"""
    
    # Sample datasets CSV
    datasets_csv_content = """name,description,source_department,file_size_mb,row_count,column_count,data_quality_score,is_archived,upload_date
Network_Logs_Q4_2024,Quarterly network security logs,IT,450.7,125000,18,0.88,0,2024-01-10 08:00:00
Employee_Access_Records,Employee system access logs,HR,89.2,25000,12,0.95,0,2024-01-09 09:15:00
Financial_Transactions_2023,Annual financial records,Finance,320.1,85000,22,0.92,1,2024-01-08 10:30:00
Customer_Support_Tickets,Customer support interactions,Support,156.8,45000,15,0.85,0,2024-01-11 11:45:00
Server_Performance_Metrics,Server performance data,IT,78.3,18000,10,0.90,0,2024-01-12 13:20:00"""
    
    # Sample IT tickets CSV
    tickets_csv_content = """title,description,assignee,reporter,status,priority,category,date_created
VPN Connection Issues,Users reporting VPN disconnections,mike_admin,HR_Department,In Progress,High,Network,2024-01-15 08:30:00
Software License Renewal,Adobe licenses expiring,anna_it,Marketing_Team,Waiting for User,Medium,Software,2024-01-14 10:15:00
Password Reset Request,User locked out of account,tom_support,Sales_Dept,Resolved,Low,Access,2024-01-13 14:45:00
Server Hardware Failure,File server hardware issues,network_team,IT_Infrastructure,Assigned,Urgent,Hardware,2024-01-15 09:00:00
Email Delivery Delays,External emails delayed,email_admin,All_Users,New,High,Email,2024-01-14 16:20:00"""
    
    csv_files = {
        'cyber_incidents.csv': cyber_csv_content,
        'datasets_metadata.csv': datasets_csv_content,
        'it_tickets.csv': tickets_csv_content
    }
    
    created_files = []
    for filename, content in csv_files.items():
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(content)
            created_files.append(filename)
            print(f"📝 Created sample file: {filename}")
    
    return created_files

def load_data_from_csv_files(db):
    """Load data from CSV files into database tables."""
    print("\n" + "="*50)
    print("📁 LOADING DATA FROM CSV FILES")
    print("="*50)
    
    csv_mapping = {
        'cyber_incidents.csv': 'cyber_incidents',
        'datasets_metadata.csv': 'datasets_metadata',
        'it_tickets.csv': 'it_tickets'
    }
    
    results = {}
    
    for csv_file, table_name in csv_mapping.items():
        if os.path.exists(csv_file):
            if db.load_csv_data(csv_file, table_name):
                results[table_name] = "✅ Success"
            else:
                results[table_name] = "❌ Failed"
        else:
            print(f"⚠️  CSV file not found: {csv_file}")
            results[table_name] = "⚠️ File Missing"
    
    return results

def load_data_directly(db):
    """Load sample data directly using CRUD methods."""
    print("\n" + "="*50)
    print("📥 LOADING SAMPLE DATA DIRECTLY")
    print("="*50)
    
    return db.load_sample_data()

def display_current_data(db):
    """Display current data counts from all tables."""
    print("\n" + "="*50)
    print("📊 CURRENT DATABASE STATISTICS")
    print("="*50)
    
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    
    for table in tables:
        try:
            count_result = db.execute_query(f"SELECT COUNT(*) FROM {table}")
            count = count_result[0][0] if count_result else 0
            print(f"📈 {table:20} : {count:3} records")
        except Exception as e:
            print(f"❌ Error counting {table}: {e}")

def main():
    """Main function to load sample data."""
    print("🚀 WEEK 8: SAMPLE DATA LOADER")
    print("Loading demonstration data into all domain tables")
    
    # Create sample CSV files
    created_files = create_sample_csv_files()
    if created_files:
        print(f"\n✅ Created {len(created_files)} sample CSV files")
    
    # Initialize database
    db = DatabaseManager()
    db.create_tables()  # Ensure tables exist
    
    # Ask user for preferred loading method
    print("\nChoose data loading method:")
    print("1. Load from CSV files")
    print("2. Load sample data directly")
    print("3. Both methods")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        # Load from CSV files
        csv_results = load_data_from_csv_files(db)
        print("\nCSV Loading Results:")
        for table, result in csv_results.items():
            print(f"  {table:20} : {result}")
    
    if choice in ['2', '3']:
        # Load data directly
        direct_results = load_data_directly(db)
        print(f"\nDirect Loading Results: {direct_results}")
    
    # Display final data counts
    display_current_data(db)
    
    # Close database connection
    db.close()
    
    print("\n✅ Sample data loading completed!")
    print("\n🎯 Next steps:")
    print("   - Run your CRUD operations script to test the data")
    print("   - Use the data for your Streamlit dashboard")
    print("   - Modify the sample data as needed for your analysis")

if __name__ == "__main__":
    main()