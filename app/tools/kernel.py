
from langchain.tools import Tool


# Update the import to use the correct path
from app.tools.file_tools import (
    create_file, write_file, read_file, list_files, 
    show_current_directory, parse_input_string, 
    PROJECTS_DIR, file_exists, execute_terminal_command,
    is_command_safe, rename_files_in_directory, execute_rename_command,
    safe_delete_file
)
from app.tools.web_tool import searchOnline
from app.tools.agentic_db_query import (
    create_database, list_databases, execute_query,
    create_table, list_tables, describe_table,
    insert_data, delete_database
)
tools = [
    Tool(
        name="Delete File",
        func=lambda input: safe_delete_file(**parse_input_string(input)),
        description=f"Delete a file in {PROJECTS_DIR}. Usage: filepath=example.txt"
    ),
    Tool(
        name="Rename File",
        func=lambda input: execute_rename_command(**parse_input_string(input)),
        description="Rename a file in the projects directory. Usage: old_name=oldfile.txt, new_name=newfile.txt"
    ),
    Tool(
        name="Rename Files",
        func=lambda input: rename_files_in_directory(PROJECTS_DIR, parse_input_string(input).get('suffix', '_one')),
        description="Rename all files in the projects directory by adding a suffix. Usage: suffix=_new"
    ),
    Tool(
        name="Execute Terminal Command",
        func=lambda input: execute_terminal_command(**parse_input_string(input)) if is_command_safe(parse_input_string(input).get("command", "")) else "Command rejected for security reasons",
        description="Execute a terminal command. Usage: command='ls -l', [cwd=path], [timeout=30]"
    ),
    Tool(
        name="Create File",
        func=lambda input: create_file(**parse_input_string(input)),
        description=f"Create a file in {PROJECTS_DIR}. Usage: filename=example.txt"
    ),
    Tool(
        name="Write File",
        func=lambda input: write_file(**parse_input_string(input)),
        description=f"Write content to a file in {PROJECTS_DIR}. Usage: filepath=example.txt, content='Hello World'"
    ),
    Tool(
        name="Read File",
        func=lambda input: read_file(**parse_input_string(input)),
        description=f"Read a file from {PROJECTS_DIR}. Usage: filepath=example.txt"
    ),
    Tool(
        name="List Files",
        func=lambda input: list_files(**parse_input_string(input)),
        description=f"List files in {PROJECTS_DIR}"
    ),
    Tool(
        name="File Exists",
        func=lambda input: file_exists(**parse_input_string(input)),
        description=f"Check if file exists in {PROJECTS_DIR}. Usage: filepath=example.txt"
    ),
    Tool(
        name="Show Current Directory",
        func=lambda input: show_current_directory(**parse_input_string(input)),
        description="Show the Projects directory path"
    ),
    Tool(
        name="Search Online",
        func=lambda input: searchOnline(input),
        description="Search the web for information on a given query. Usage: query='How to create a website'"
    ),
    Tool(
        name="Create Database",
        func=lambda input: create_database(**parse_input_string(input)),
        description="Create a new SQLite database. Usage: db_name=mydatabase"
    ),
    Tool(
        name="List Databases",
        func=lambda input: list_databases(**parse_input_string(input)),
        description="List all available databases in the databases directory"
    ),
    Tool(
        name="Execute SQL Query",
        func=lambda input: execute_query(**parse_input_string(input)),
        description="Execute a SQL query on a database. Usage: db_name=mydatabase, query='SELECT * FROM users'"
    ),
    Tool(
        name="Create Table",
        func=lambda input: create_table(**parse_input_string(input)),
        description="Create a table in a database. Usage: db_name=mydatabase, table_name=users, columns='id INTEGER PRIMARY KEY, name TEXT, email TEXT'"
    ),
    Tool(
        name="List Tables",
        func=lambda input: list_tables(**parse_input_string(input)),
        description="List all tables in a database. Usage: db_name=mydatabase"
    ),
    Tool(
        name="Describe Table",
        func=lambda input: describe_table(**parse_input_string(input)),
        description="Describe the structure of a table. Usage: db_name=mydatabase, table_name=users"
    ),
    Tool(
        name="Insert Data",
        func=lambda input: insert_data(**parse_input_string(input)),
        description="Insert data into a table. Usage: db_name=mydatabase, table_name=users, columns='name, email', values=\"'John Doe', 'john@example.com'\""
    ),
    Tool(
        name="Delete Database",
        func=lambda input: delete_database(**parse_input_string(input)),
        description="Delete a database file. Usage: db_name=mydatabase"
    )
]
