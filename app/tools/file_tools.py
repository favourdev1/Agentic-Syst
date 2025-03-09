import os
import subprocess
from typing import Optional

PROJECTS_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "Ai Stuff", "AgenticSystem", "Projects")

def clean_content(content):
    """Clean and format content before writing to file."""
    if not isinstance(content, str):
        return str(content)
    
    # Remove surrounding quotes if they exist
    if (content.startswith('"') and content.endswith('"')) or \
       (content.startswith("'") and content.endswith("'")):
        content = content[1:-1]
    
    # Replace literal \n with actual newlines
    content = content.replace('\\n', '\n')
    
    # Handle HTML content specifically
    if content.strip().startswith('<!DOCTYPE') or content.strip().startswith('<html'):
        # Ensure proper HTML formatting
        content = content.replace('\\t', '\t')
        content = content.replace('\\r', '')
        
    return content

def create_file(**kwargs):  
    print("Received kwargs:", kwargs)  # Debugging output
    try:
        filename = kwargs.get("filename", "new_file.txt")
        target_path = os.path.abspath(os.path.join(PROJECTS_DIR, filename))
        
        if os.path.commonpath([target_path, PROJECTS_DIR]) != PROJECTS_DIR:
            return f"Access denied: You can only create files inside {PROJECTS_DIR}"
        
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        try:
            with open(target_path, "w") as f:
                f.write("")  
            return f"File '{filename}' created successfully in {PROJECTS_DIR}"
        except Exception as e:
            return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def list_files(**kwargs):
    try:
        return "\n".join(os.listdir(PROJECTS_DIR)) or "No files found."
    except FileNotFoundError:
        return "Error: Projects directory not found."

def read_file(**kwargs):
    """
    Read the content of a file specified by the 'filepath' argument.

    Args:
        filepath (str): The relative path to the file within the projects directory.

    Returns:
        str: The content of the file, or an error message if the file cannot be read.
    """
    filepath = kwargs.get("filepath")
    if not filepath:
        return "Error: Filepath required."
        
    target_file = os.path.abspath(os.path.join(PROJECTS_DIR, filepath))
    
    if not target_file.startswith(PROJECTS_DIR):
        return f"Error: File not found or access denied. Files must be inside {PROJECTS_DIR}"
        
    try:
        with open(target_file, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(**kwargs):
    """
    Write content to a file in the projects directory.

    Args:
        kwargs: A dictionary containing 'filepath' and 'content'.

    Returns:
        A string indicating success or the type of error encountered.
    """
    filepath = kwargs.get("filepath")
    content = kwargs.get("content", "")

    if not filepath:
        return "Error: Filepath required."

    target_file = os.path.abspath(os.path.join(PROJECTS_DIR, filepath))

    if not target_file.startswith(PROJECTS_DIR):
        return f"Access denied: You can only write files inside {PROJECTS_DIR}"

    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        cleaned_content = clean_content(content)
        
        with open(target_file, "w", encoding="utf-8") as file:
            file.write(cleaned_content)
        return f"Successfully wrote content to '{filepath}'"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

def show_current_directory(**_):
    """
    Return the path to the projects directory.

    Returns:
        str: The absolute path to the projects directory.
    """
    return PROJECTS_DIR

def show_current_directory(**kwargs):
    return PROJECTS_DIR

def parse_input_string(input_str):
    """Convert string input to dictionary for tool functions."""
    if isinstance(input_str, dict):
        return input_str

    parts = {}
    try:
        if '=' not in input_str:
            return {'input': input_str}
            
        # Split by comma only if it's not inside quotes
        pairs = []
        current = []
        in_quotes = False
        quote_char = None
        
        for char in input_str:
            if char in ['"', "'"]:
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
            elif char == ',' and not in_quotes:
                pairs.append(''.join(current))
                current = []
                continue
            current.append(char)
        
        if current:
            pairs.append(''.join(current))

        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                # Remove surrounding quotes and whitespace
                value = value.strip()
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                parts[key.strip()] = value
    except Exception as e:
        print(f"Error parsing input: {e}")
        parts = {'input': input_str}
    return parts

# check if file exist
def file_exists(**kwargs):
    """Check if a file exists in the projects directory."""
    filepath = kwargs.get("filepath")
    if not filepath:
        return "Error: Filepath required."
    target_file = os.path.abspath(os.path.join(PROJECTS_DIR, filepath))
    return str(os.path.exists(target_file))

def execute_terminal_command(**kwargs):
    """Execute a terminal command and return its output."""
    command = kwargs.get("command")
    if not command:
        return "Error: Command required."
    
    cwd = kwargs.get("cwd", PROJECTS_DIR)
    timeout = kwargs.get("timeout", 30)
    
    # Only allow operations within PROJECTS_DIR
    if not os.path.abspath(cwd).startswith(PROJECTS_DIR):
        return "Error: Operations are only allowed within the Projects directory"
    
    # Parse the command to ensure it only affects files in PROJECTS_DIR
    cmd_parts = command.split()
    if cmd_parts[0] in ['mv', 'cp', 'rm', 'touch']:
        # Check all file arguments in the command
        for arg in cmd_parts[1:]:
            if arg.startswith('-'):  # Skip command options
                continue
            arg_path = os.path.abspath(os.path.join(cwd, arg))
            if not arg_path.startswith(PROJECTS_DIR):
                return f"Error: Cannot access paths outside of {PROJECTS_DIR}"
    
    try:
        # Run the command with working directory set to PROJECTS_DIR
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=PROJECTS_DIR  # Force working directory to PROJECTS_DIR
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            if process.returncode == 0:
                output = stdout.strip()
                return f"Command executed successfully:\n{output}" if output else "Command executed successfully (no output)"
            else:
                return f"Command failed with error:\n{stderr.strip()}"
        except subprocess.TimeoutExpired:
            process.kill()
            return f"Command timed out after {timeout} seconds"
            
    except Exception as e:
        return f"Error executing command: {str(e)}"

# Add security check for commands
def is_command_safe(command: str) -> bool:
    """
    Enhanced security check for commands.
    Whitelist approach - only allow specific safe commands
    """
    # List of allowed basic commands
    allowed_commands = [
        'ls', 'mv', 'cp', 'pwd', 'echo',
        'mkdir', 'touch', 'cat', 'find',
        'basename', 'dirname', 'rm'  # Added rm for single file deletion
    ]
    
    # List of dangerous patterns
    forbidden_patterns = [
        "rm -rf", "rmdir", "del", "format",
        ">", ">>", # redirections
        "|", # pipes
        "&", # background execution
        "sudo", # privilege escalation
        ";", # command chaining
        "`", # command substitution
        "$(" # command substitution
    ]
    
    command_lower = command.lower()
    
    # Special check for rm command to ensure it's not recursive
    if command_lower.startswith('rm '):
        if any(flag in command_lower for flag in ['-r', '-rf', '-fr', '-f', '--recursive']):
            return False
        
    # Check if command starts with an allowed command
    is_allowed = any(command_lower.startswith(cmd + ' ') or command_lower == cmd 
                    for cmd in allowed_commands)
    
    # Check for forbidden patterns
    has_forbidden = any(pattern in command_lower for pattern in forbidden_patterns)
    
    return is_allowed and not has_forbidden

# Add a new function specifically for safe file operations
def safe_rename_file(old_path: str, new_path: str) -> str:
    """Safely rename a file within PROJECTS_DIR."""
    old_abs_path = os.path.abspath(os.path.join(PROJECTS_DIR, old_path))
    new_abs_path = os.path.abspath(os.path.join(PROJECTS_DIR, new_path))
    
    # Verify both paths are within PROJECTS_DIR
    if not (old_abs_path.startswith(PROJECTS_DIR) and new_abs_path.startswith(PROJECTS_DIR)):
        return "Error: Can only rename files within the Projects directory"
        
    try:
        os.rename(old_abs_path, new_abs_path)
        return f"Successfully renamed '{old_path}' to '{new_path}'"
    except Exception as e:
        return f"Error renaming file: {str(e)}"

def rename_files_in_directory(directory: str, suffix: str = "_one") -> str:
    """
    Safely rename files in a directory by adding a suffix.
    Returns a string describing the operations performed.
    """
    try:
        results = []
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                name, ext = os.path.splitext(filename)
                if not name.endswith(suffix):  # Prevent double-renaming
                    new_name = f"{name}{suffix}{ext}"
                    os.rename(
                        os.path.join(directory, filename),
                        os.path.join(directory, new_name)
                    )
                    results.append(f"Renamed '{filename}' to '{new_name}'")
        
        if results:
            return "\n".join(results)
        return "No files were renamed"
        
    except Exception as e:
        return f"Error renaming files: {str(e)}"

def execute_rename_command(**kwargs):
    """Execute a rename command specifically for files in PROJECTS_DIR."""
    old_name = kwargs.get("old_name")
    new_name = kwargs.get("new_name")
    
    if not old_name or not new_name:
        return "Error: Both old_name and new_name are required"
    
    old_path = os.path.join(PROJECTS_DIR, old_name)
    new_path = os.path.join(PROJECTS_DIR, new_name)
    
    # Verify the files are within PROJECTS_DIR
    if not (os.path.abspath(old_path).startswith(PROJECTS_DIR) and 
            os.path.abspath(new_path).startswith(PROJECTS_DIR)):
        return "Error: Can only rename files within the Projects directory"
    
    # Check if source file exists
    if not os.path.exists(old_path):
        return f"Error: Source file '{old_name}' does not exist"
    
    try:
        os.rename(old_path, new_path)
        return f"Successfully renamed '{old_name}' to '{new_name}'"
    except Exception as e:
        return f"Error renaming file: {str(e)}"

def safe_delete_file(**kwargs):
    """Safely delete a file within PROJECTS_DIR."""
    filepath = kwargs.get("filepath")
    if not filepath:
        return "Error: Filepath required."
    
    target_file = os.path.abspath(os.path.join(PROJECTS_DIR, filepath))
    
    # Verify path is within PROJECTS_DIR
    if not target_file.startswith(PROJECTS_DIR):
        return "Error: Can only delete files within the Projects directory"
    
    # Check if file exists
    if not os.path.exists(target_file):
        return f"Error: File '{filepath}' does not exist"
    
    # Verify it's a file, not a directory
    if not os.path.isfile(target_file):
        return f"Error: '{filepath}' is not a file"
    
    try:
        os.remove(target_file)
        return f"Successfully deleted file '{filepath}'"
    except Exception as e:
        return f"Error deleting file: {str(e)}"
