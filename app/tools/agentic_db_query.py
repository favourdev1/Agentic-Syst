import os
import sqlite3
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

# Database directory within Projects
PROJECTS_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Ai Stuff", "AgenticSystem", "Projects")
DB_DIR = os.path.join(PROJECTS_DIR, "databases")

def ensure_db_directory():
    """Ensure the databases directory exists."""
    os.makedirs(DB_DIR, exist_ok=True)
    return DB_DIR

def get_db_path(db_name: str) -> str:
    """Get the full path to a database file."""
    ensure_db_directory()
    if not db_name.endswith('.db'):
        db_name += '.db'
    return os.path.join(DB_DIR, db_name)

def create_database(**kwargs) -> str:
    """
    Create a new SQLite database.
    
    Args:
        db_name (str): Name of the database to create
    
    Returns:
        str: Success or error message
    """
    db_name = kwargs.get("db_name")
    if not db_name:
        return "Error: Database name required."
    
    try:
        db_path = get_db_path(db_name)
        
        if os.path.exists(db_path):
            return f"Database '{db_name}' already exists at {db_path}"
        
        # Create database by connecting to it
        conn = sqlite3.connect(db_path)
        conn.close()
        
        return f"Database '{db_name}' created successfully at {db_path}"
    except Exception as e:
        return f"Error creating database: {str(e)}"

def list_databases(**kwargs) -> str:
    """
    List all databases in the databases directory.
    
    Returns:
        str: List of database files or error message
    """
    try:
        ensure_db_directory()
        db_files = [f for f in os.listdir(DB_DIR) if f.endswith('.db')]
        
        if not db_files:
            return "No databases found."
        
        return "Databases:\n" + "\n".join(f"- {db}" for db in db_files)
    except Exception as e:
        return f"Error listing databases: {str(e)}"

def execute_query(**kwargs) -> str:
    """
    Execute a SQL query on a specified database.
    
    Args:
        db_name (str): Name of the database
        query (str): SQL query to execute
    
    Returns:
        str: Query results or error message
    """
    db_name = kwargs.get("db_name")
    query = kwargs.get("query")
    
    if not db_name:
        return "Error: Database name required."
    if not query:
        return "Error: SQL query required."
    
    # Security check for dangerous operations
    query_lower = query.lower().strip()
    dangerous_keywords = ['drop database', 'drop schema']
    
    if any(keyword in query_lower for keyword in dangerous_keywords):
        return "Error: Potentially dangerous operation blocked for security reasons."
    
    try:
        db_path = get_db_path(db_name)
        
        if not os.path.exists(db_path):
            return f"Error: Database '{db_name}' does not exist. Create it first."
        
        # Use SQLAlchemy for safer query execution
        engine = create_engine(f'sqlite:///{db_path}')
        
        with engine.connect() as connection:
            result = connection.execute(text(query))
            
            # If it's a SELECT query, fetch and return results
            if query_lower.startswith('select'):
                rows = result.fetchall()
                if not rows:
                    return "Query executed successfully. No rows returned."
                
                # Format results as a table
                columns = list(result.keys())
                output = [" | ".join(columns)]
                output.append("-" * len(output[0]))
                
                for row in rows:
                    output.append(" | ".join(str(val) for val in row))
                
                return "\n".join(output)
            else:
                # For INSERT, UPDATE, DELETE, etc.
                connection.commit()
                return f"Query executed successfully. Rows affected: {result.rowcount}"
        
    except SQLAlchemyError as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error executing query: {str(e)}"

def create_table(**kwargs) -> str:
    """
    Create a table in a specified database.
    
    Args:
        db_name (str): Name of the database
        table_name (str): Name of the table to create
        columns (str): Column definitions (e.g., "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")
    
    Returns:
        str: Success or error message
    """
    db_name = kwargs.get("db_name")
    table_name = kwargs.get("table_name")
    columns = kwargs.get("columns")
    
    if not db_name:
        return "Error: Database name required."
    if not table_name:
        return "Error: Table name required."
    if not columns:
        return "Error: Column definitions required."
    
    try:
        db_path = get_db_path(db_name)
        
        if not os.path.exists(db_path):
            return f"Error: Database '{db_name}' does not exist. Create it first."
        
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        
        engine = create_engine(f'sqlite:///{db_path}')
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
        
        return f"Table '{table_name}' created successfully in database '{db_name}'"
    except Exception as e:
        return f"Error creating table: {str(e)}"

def list_tables(**kwargs) -> str:
    """
    List all tables in a specified database.
    
    Args:
        db_name (str): Name of the database
    
    Returns:
        str: List of tables or error message
    """
    db_name = kwargs.get("db_name")
    
    if not db_name:
        return "Error: Database name required."
    
    try:
        db_path = get_db_path(db_name)
        
        if not os.path.exists(db_path):
            return f"Error: Database '{db_name}' does not exist."
        
        engine = create_engine(f'sqlite:///{db_path}')
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            return f"No tables found in database '{db_name}'."
        
        return f"Tables in '{db_name}':\n" + "\n".join(f"- {table}" for table in tables)
    except Exception as e:
        return f"Error listing tables: {str(e)}"

def describe_table(**kwargs) -> str:
    """
    Describe the structure of a table.
    
    Args:
        db_name (str): Name of the database
        table_name (str): Name of the table
    
    Returns:
        str: Table structure or error message
    """
    db_name = kwargs.get("db_name")
    table_name = kwargs.get("table_name")
    
    if not db_name:
        return "Error: Database name required."
    if not table_name:
        return "Error: Table name required."
    
    try:
        db_path = get_db_path(db_name)
        
        if not os.path.exists(db_path):
            return f"Error: Database '{db_name}' does not exist."
        
        engine = create_engine(f'sqlite:///{db_path}')
        inspector = inspect(engine)
        
        if table_name not in inspector.get_table_names():
            return f"Error: Table '{table_name}' does not exist in database '{db_name}'."
        
        columns = inspector.get_columns(table_name)
        
        output = [f"Table: {table_name}"]
        output.append("Columns:")
        
        for col in columns:
            col_info = f"  - {col['name']}: {col['type']}"
            if col.get('nullable') is False:
                col_info += " NOT NULL"
            if col.get('primary_key'):
                col_info += " PRIMARY KEY"
            output.append(col_info)
        
        return "\n".join(output)
    except Exception as e:
        return f"Error describing table: {str(e)}"

def insert_data(**kwargs) -> str:
    """
    Insert data into a table.
    
    Args:
        db_name (str): Name of the database
        table_name (str): Name of the table
        columns (str): Comma-separated column names (e.g., "name, age")
        values (str): Comma-separated values (e.g., "'John', 25")
    
    Returns:
        str: Success or error message
    """
    db_name = kwargs.get("db_name")
    table_name = kwargs.get("table_name")
    columns = kwargs.get("columns")
    values = kwargs.get("values")
    
    if not db_name:
        return "Error: Database name required."
    if not table_name:
        return "Error: Table name required."
    if not values:
        return "Error: Values required."
    
    try:
        db_path = get_db_path(db_name)
        
        if not os.path.exists(db_path):
            return f"Error: Database '{db_name}' does not exist."
        
        if columns:
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        else:
            query = f"INSERT INTO {table_name} VALUES ({values})"
        
        engine = create_engine(f'sqlite:///{db_path}')
        with engine.connect() as connection:
            connection.execute(text(query))
            connection.commit()
        
        return f"Data inserted successfully into table '{table_name}'"
    except Exception as e:
        return f"Error inserting data: {str(e)}"

def delete_database(**kwargs) -> str:
    """
    Delete a database file.
    
    Args:
        db_name (str): Name of the database to delete
    
    Returns:
        str: Success or error message
    """
    db_name = kwargs.get("db_name")
    
    if not db_name:
        return "Error: Database name required."
    
    try:
        db_path = get_db_path(db_name)
        
        if not os.path.exists(db_path):
            return f"Error: Database '{db_name}' does not exist."
        
        os.remove(db_path)
        return f"Database '{db_name}' deleted successfully"
    except Exception as e:
        return f"Error deleting database: {str(e)}"
