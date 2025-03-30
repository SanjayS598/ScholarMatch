import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

user_input = input("Enter your query: ")

response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "web_search_preview"}],
    input=user_input
)

print(response.output_text)


