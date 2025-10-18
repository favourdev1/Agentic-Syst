#!/usr/bin/env python3
"""
Example of using the database tools programmatically.

This demonstrates how the AI agent would use the database tools
to manage and query SQLite databases.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.tools.file_tools import parse_input_string
from app.tools.agentic_db_query import (
    create_database, list_databases, execute_query,
    create_table, list_tables, describe_table,
    insert_data, delete_database
)

def example_workflow():
    """Demonstrate a typical database workflow"""
    
    print("=" * 70)
    print("Database Tools Example Workflow")
    print("=" * 70)
    
    # Step 1: Create a database
    print("\n📁 Step 1: Creating a new database for a contact management system...")
    result = create_database(db_name="contacts")
    print(result)
    
    # Step 2: Create a contacts table
    print("\n📋 Step 2: Creating a 'contacts' table...")
    result = create_table(
        db_name="contacts",
        table_name="contacts",
        columns="id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT, phone TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    )
    print(result)
    
    # Step 3: Insert sample contacts
    print("\n➕ Step 3: Adding sample contacts...")
    contacts = [
        ("'John Doe', 'john.doe@example.com', '555-0100'"),
        ("'Jane Smith', 'jane.smith@example.com', '555-0101'"),
        ("'Bob Johnson', 'bob.johnson@example.com', '555-0102'"),
        ("'Alice Williams', 'alice.w@example.com', '555-0103'"),
    ]
    
    for contact_data in contacts:
        result = insert_data(
            db_name="contacts",
            table_name="contacts",
            columns="name, email, phone",
            values=contact_data
        )
        print(f"  {result}")
    
    # Step 4: Query all contacts
    print("\n📊 Step 4: Querying all contacts...")
    result = execute_query(
        db_name="contacts",
        query="SELECT * FROM contacts"
    )
    print(result)
    
    # Step 5: Query specific contacts
    print("\n🔍 Step 5: Finding contacts with '555-010' phone numbers...")
    result = execute_query(
        db_name="contacts",
        query="SELECT name, phone FROM contacts WHERE phone LIKE '555-010%'"
    )
    print(result)
    
    # Step 6: Update a contact
    print("\n✏️  Step 6: Updating John Doe's phone number...")
    result = execute_query(
        db_name="contacts",
        query="UPDATE contacts SET phone = '555-9999' WHERE name = 'John Doe'"
    )
    print(result)
    
    # Step 7: Verify the update
    print("\n✅ Step 7: Verifying the update...")
    result = execute_query(
        db_name="contacts",
        query="SELECT name, phone FROM contacts WHERE name = 'John Doe'"
    )
    print(result)
    
    # Step 8: Create a notes table
    print("\n📝 Step 8: Creating a 'notes' table for contact notes...")
    result = create_table(
        db_name="contacts",
        table_name="notes",
        columns="id INTEGER PRIMARY KEY AUTOINCREMENT, contact_id INTEGER, note TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    )
    print(result)
    
    # Step 9: List all tables
    print("\n📑 Step 9: Listing all tables in the database...")
    result = list_tables(db_name="contacts")
    print(result)
    
    # Step 10: Describe the contacts table structure
    print("\n🔍 Step 10: Describing the 'contacts' table structure...")
    result = describe_table(db_name="contacts", table_name="contacts")
    print(result)
    
    # Step 11: List all databases
    print("\n💾 Step 11: Listing all databases...")
    result = list_databases()
    print(result)
    
    print("\n" + "=" * 70)
    print("Example workflow completed!")
    print("=" * 70)
    print("\nNote: The database is still active. Use delete_database(db_name='contacts')")
    print("      if you want to remove it.")
    
    # Optional: Uncomment to clean up
    # print("\n🗑️  Cleaning up: Deleting the contacts database...")
    # result = delete_database(db_name="contacts")
    # print(result)

if __name__ == "__main__":
    example_workflow()
