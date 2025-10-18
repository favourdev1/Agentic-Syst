# Database Query Tools

This module provides database query capabilities for the Agentic System using SQLite databases.

## Overview

The `agentic_db_query.py` module adds database management and query functionality to the AI agent, allowing it to create, manage, and query SQLite databases stored in the Projects directory.

## Features

- **Database Management**: Create and delete SQLite databases
- **Table Operations**: Create tables, list tables, and describe table structure
- **Data Manipulation**: Insert, query, update, and delete data
- **Security**: Built-in safety checks to prevent dangerous operations
- **Integration**: Seamlessly integrated with the existing tool system

## Available Tools

### 1. Create Database
Creates a new SQLite database in the databases directory.

**Usage:**
```
db_name=mydatabase
```

### 2. List Databases
Lists all available databases in the databases directory.

**Usage:** No parameters required

### 3. Execute SQL Query
Executes a SQL query on a specified database.

**Usage:**
```
db_name=mydatabase, query='SELECT * FROM users'
```

**Supported Operations:**
- SELECT queries
- INSERT statements
- UPDATE statements
- DELETE statements
- CREATE TABLE statements
- DROP TABLE statements (with safety checks)

### 4. Create Table
Creates a table in a specified database.

**Usage:**
```
db_name=mydatabase, table_name=users, columns='id INTEGER PRIMARY KEY, name TEXT, email TEXT'
```

### 5. List Tables
Lists all tables in a specified database.

**Usage:**
```
db_name=mydatabase
```

### 6. Describe Table
Describes the structure of a table, showing column names, types, and constraints.

**Usage:**
```
db_name=mydatabase, table_name=users
```

### 7. Insert Data
Inserts data into a table.

**Usage:**
```
db_name=mydatabase, table_name=users, columns='name, email', values="'John Doe', 'john@example.com'"
```

### 8. Delete Database
Deletes a database file.

**Usage:**
```
db_name=mydatabase
```

## Security Features

- All databases are stored in a dedicated `databases` subdirectory within the Projects folder
- Dangerous operations like `DROP DATABASE` are blocked
- Path validation ensures all operations stay within the designated directory
- SQLAlchemy is used for safe query execution with parameterization support

## Example Workflow

1. **Create a database:**
   ```
   Create Database: db_name=contacts
   ```

2. **Create a table:**
   ```
   Create Table: db_name=contacts, table_name=people, columns='id INTEGER PRIMARY KEY, name TEXT, phone TEXT'
   ```

3. **Insert data:**
   ```
   Insert Data: db_name=contacts, table_name=people, columns='name, phone', values="'John Doe', '555-1234'"
   ```

4. **Query data:**
   ```
   Execute SQL Query: db_name=contacts, query='SELECT * FROM people'
   ```

5. **Update data:**
   ```
   Execute SQL Query: db_name=contacts, query="UPDATE people SET phone='555-5678' WHERE name='John Doe'"
   ```

## Technical Details

- **Database Engine**: SQLite 3
- **ORM**: SQLAlchemy 2.0.38
- **Storage Location**: `~/Desktop/Ai Stuff/AgenticSystem/Projects/databases/`
- **File Extension**: `.db`

## Error Handling

The module includes comprehensive error handling for:
- Missing required parameters
- Non-existent databases or tables
- SQL syntax errors
- Permission issues
- Database operation failures

All errors return descriptive messages to help users understand and resolve issues.

## Integration

The database tools are automatically registered in `app/tools/kernel.py` and are available to the AI agent alongside other tools like file operations and web search.
