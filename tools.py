import os

PROJECTS_DIR = "/Users/user/Desktop/Ai Stuff/AgenticSystem/Projects"

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
        
        if not target_path.startswith(PROJECTS_DIR):
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
    filepath = kwargs.get("filepath")
    if not filepath:
        return "Error: Filepath required."
    target_file = os.path.abspath(os.path.join(PROJECTS_DIR, filepath))
    if not target_file.startswith(PROJECTS_DIR) or not os.path.exists(target_file):
        return f"Error: File not found or access denied. Files must be inside {PROJECTS_DIR}"
    try:
        with open(target_file, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(**kwargs):
    filepath = kwargs.get("filepath")
    content = kwargs.get("content", "")

    if not filepath:
        return "Error: Filepath required."

    target_file = os.path.abspath(os.path.join(PROJECTS_DIR, filepath))

    if not target_file.startswith(PROJECTS_DIR):
        return f"Access denied: You can only write files inside {PROJECTS_DIR}"

    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        
        # Clean and format the content
        cleaned_content = clean_content(content)
        
        with open(target_file, "w", encoding="utf-8") as file:
            file.write(cleaned_content)
        return f"Successfully wrote content to '{filepath}'"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

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
