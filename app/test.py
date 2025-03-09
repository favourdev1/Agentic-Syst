import openai 
import httpx

# Ensure OpenAI client uses LM Studio
client = openai.OpenAI(
    base_url="http://localhost:1234/v1",  # Ensure LM Studio is running on this port
    api_key="lm-studio"  # Placeholder key (not actually used)
)

    
# Testing the connection 
response = client.chat.completions.create(
    model="deepseek-r1-distill-qwen-1.5b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        # {"role": "user", "content": "What do you do?"},
    ]
)
print(response.choices[0].message.content)