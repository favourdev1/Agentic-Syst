import os
import sys
import warnings
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import MessagesPlaceholder
from langchain_core.memory import BaseMemory
from langchain.memory import ConversationBufferMemory

from tools import create_file, write_file, read_file, list_files, show_current_directory, parse_input_string, PROJECTS_DIR, file_exists

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

# Instead of suppressing specific warnings, we'll use a simpler approach
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Step 1: Connect to LM Studio and configure the agent
llm = ChatOpenAI(
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="lm-studio",
    model_name="qwen2.5-coder-7b-instruct-mlx",
    temperature=0
)

# Step 2: Define Tools with Proper Argument Handling
tools = [
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
]

# Step 3: Initialize the Agent with Proper Argument Passing
SYSTEM_PROMPT = '''You are an AI assistant specialized in file management.

IMPORTANT: Always respond in this exact format:
Thought: [Your reasoning]
Action: [Tool name]
Action Input: [Tool parameters]
Observation: [Tool result]

Example task - Writing a poem:
Thought: I need to write a poem and save it to a file
Action: Create File
Action Input: filename=poem.txt
Observation: File created successfully
Thought: Now I'll write the poem to the file
Action: Write File
Action Input: filepath=poem.txt, content='[The poem content]'
Observation: Content written successfully
Thought: Let me verify the content was written correctly
Action: Read File
Action Input: filepath=poem.txt
Observation: [File content]

Available tools:
- Create File: Creates a new file
- Write File: Writes content to a file
- Read File: Reads content from a file
- List Files: Lists files in directory
- Show Current Directory: Shows current path
- File Exists: Check if file exists

For every task:
1. Create a plan structure to accomplish the task
2. Execute the plan step by step
3. Verify each step is successful
4. If you notice an error, try to correct it
5. If you can't correct the error, report it to the user
6. Always provide a clear explanation of your actions
7. DO NOT stop until all steps are complete

IMPORTANT: Never stop at just creating a file - always complete all steps of the task.
If the task involves writing content, you must write the content and verify it.
Only provide a Final Answer after completing ALL steps.

Remember: Always use exact tool names and proper key=value format for inputs.
Make decisions where possible, unless the user provides you additional information.
'''

# Define the human message template
HUMAN_MESSAGE_TEMPLATE = """
Task: {input}

Remember to:
1. Follow the exact format (Thought/Action/Action Input/Observation)
2. Use the available tools correctly
3. Complete the task step by step

repeat and rinse until the task is completed

You have full power to do as you wish 
"""

# Update memory implementation
memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history",
    output_key=None,  # Set to None since we're not using a specific output key
)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Changed from OPENAI_FUNCTIONS
    verbose=True,
    handle_parsing_errors=True,
    memory=memory,
    # agent_kwargs={
    #     "system_message": SYSTEM_PROMPT,
    #     "human_message_template": HUMAN_MESSAGE_TEMPLATE,
    #     "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")]
    # },
    max_iterations=20,  # Ensure the agent has enough iterations to complete the task
    # early_stopping_method="generate"  # Only stop when the task is genuinely complete
)

# response = agent.invoke({"input": "create a very short poem about dog "})
response = agent.invoke({"input": "create a website landing page  for me. make it pretty and modularized  "})
print("\nFinal Output:")
print(response['output'])

# Step 4: Test the Agent with Error Handling
def run_agent_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = agent.run(prompt)
            print(response)
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"\nFinal error: {str(e)}")
                print("The operation could not be completed. Please try again with a different request.")
            else:
                print(f"Attempt {attempt + 1} failed. Retrying...")