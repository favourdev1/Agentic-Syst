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
from langchain.callbacks.base import BaseCallbackHandler
from app.tools.kernel import tools

# Instead of suppressing specific warnings, we'll use a simpler approach
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Step 1: Connect to LM Studio and configure the agent
llm = ChatOpenAI(
    openai_api_base="http://localhost:1234/v1",
    openai_api_key="lm-studio",
    model_name="gemma-2-2b-it",
    temperature=0,
    streaming=True  # Enable streaming
)

# Step 3: Initialize the Agent with Proper Argument Passing
SYSTEM_PROMPT = '''You are an AI assistant specialized in building webpages and handling various tasks using the tools available to you.
You can create, read, write, and delete files, execute terminal commands, and even search online when needed.

When responding to queries that don't require tools, provide a direct answer.
When tools are needed, ALWAYS use this exact format:

Thought: [Your reasoning about what needs to be done]
Action: [The tool name to use]
Action Input: [The input for the tool]
Observation: [The result of the action]
... (repeat Thought/Action/Action Input/Observation if more steps needed)
Final Answer: [Your final response to the user]

Remember:
1. Always include "Final Answer:" for your concluding response
2. Only use tools when absolutely necessary
3. Maintain exact formatting for tool usage
4. For simple questions, respond directly without tools

Do not include "None" or skip any parts of the format when using tools.'''

# Define the human message template
HUMAN_MESSAGE_TEMPLATE = """
Task: {input}

Remember to:
1. First evaluate if the task requires any tool or file operations
2. If the task can be answered directly, do so without using tools
3. Only use tools when specifically needed to complete the task
4. If using tools, follow the exact format (Thought/Action/Action Input/Observation)

The goal is to provide helpful responses while avoiding unnecessary file operations.
"""

# Update memory implementation
memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history",
    output_key=None,
)

class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self, socketio):
        super().__init__()
        self.socketio = socketio
        self.tool_used = False

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.socketio.emit('agent_update', {
            'type': 'step',
            'data': {
                'thought': 'Evaluating whether this question needs tools or can be answered directly...',
                'action': 'Thinking',
                'action_input': '',
                'observation': ''
            }
        })

    def on_llm_new_token(self, token, **kwargs):
        # Only stream tokens if we haven't used any tools
        # This helps distinguish between direct responses and tool-based responses
        if not self.tool_used:
            self.socketio.emit('agent_update', {
                'type': 'token',
                'data': {
                    'token': token
                }
            })

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.tool_used = True
        tool_name = serialized.get('name', 'Unknown tool')
        self.socketio.emit('agent_update', {
            'type': 'step',
            'data': {
                'thought': f'This task requires using a tool: {tool_name}',
                'action': 'Starting tool',
                'action_input': input_str,
                'observation': ''
            }
        })

    def on_tool_end(self, output, **kwargs):
        self.socketio.emit('agent_update', {
            'type': 'step',
            'data': {
                'thought': 'Tool operation completed',
                'action': 'Tool output',
                'action_input': '',
                'observation': str(output)
            }
        })

    def on_agent_action(self, action, **kwargs):
        self.socketio.emit('agent_update', {
            'type': 'step',
            'data': {
                'thought': action.log,
                'action': action.tool,
                'action_input': action.tool_input,
                'observation': ''
            }
        })

    def on_agent_finish(self, finish, **kwargs):
        response_type = 'direct' if not self.tool_used else 'tool-based'
        self.socketio.emit('agent_update', {
            'type': 'final',
            'data': {
                'output': finish.return_values['output'] if isinstance(finish.return_values, dict) else str(finish.return_values),
                'response_type': response_type
            }
        })
        # Reset tool usage flag for next interaction
        self.tool_used = False

def create_agent(socketio=None):
    callback_handler = StreamingCallbackHandler(socketio) if socketio else None
    
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        memory=memory,
        max_iterations=5,
        return_intermediate_steps=True,
        callbacks=[callback_handler] if callback_handler else None,
        agent_kwargs={
            "prefix": SYSTEM_PROMPT,
            "format_instructions": "When you need to use a tool, use the following format:\n\nThought: [Your reasoning]\nAction: [Tool name]\nAction Input: [Tool input]\nObservation: [Tool output]\n... (repeat until done)\nFinal Answer: [Your response]",
            "input_variables": ["input", "agent_scratchpad", "chat_history"]
        }
    )

# Don't create the agent immediately, let it be created with the socket
agent = None

