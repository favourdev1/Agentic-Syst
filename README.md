# Agentic System

A Python-based AI agent system using LangChain and LM Studio  for file management and content creation.

## Features

- File creation and management
- Content writing and reading
- Directory operations
- **Database management and querying (SQLite)**
- Web search capabilities
- Terminal command execution
- Built with LangChain and OpenAI API compatibility

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure LM Studio is running locally on port 1234

3. Run the agent:
```bash
python agent.py
```

## Project Structure

- `app.py`: Flask application with WebSocket support
- `app/controller/agent.py`: Main agent implementation with streaming
- `app/tools/`: Custom tools directory
  - `file_tools.py`: File operations
  - `web_tool.py`: Web search functionality
  - `agentic_db_query.py`: Database management tools
  - `kernel.py`: Tool registration
- `templates/`: Web UI templates
- `examples/`: Example scripts demonstrating tool usage
- `Projects/`: Directory for generated content
  - `databases/`: SQLite databases storage

## Database Tools

The system includes comprehensive database management capabilities. See [DATABASE_TOOLS.md](DATABASE_TOOLS.md) for detailed documentation.

**Quick Example:**
```bash
python examples/database_example.py
```

This demonstrates creating databases, tables, inserting data, and running queries.