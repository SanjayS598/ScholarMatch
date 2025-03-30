import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from flask import Flask, render_template

app = Flask(__name__)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load JSON input from file
json_filepath = "c:\\Users\\sssgu\\OneDrive\\Desktop\\Hoohacks\\ScholarMatch\\Backend\\Tests\\Inputs\\test_input.json"
with open(json_filepath, "r", encoding="utf-8") as f:
    data = json.load(f)

gpa = data.get("gpa", "")
age = data.get("age", "")
major = data.get("major", "")
studying_level = data.get("studying_level", "")
demographics = data.get("demographics", "")

prompt = (
    f"Find 10 scholarships for an applicant with the following details:\n"
    f"GPA: {gpa}\n"
    f"Age: {age}\n"
    f"Studying Level: {studying_level}\n"
    f"Ethnicity: {demographics}\n"
    f"Major: {major}\n\n"
)

response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "web_search_preview"}],
    input=prompt
)

# Save GPT's Markdown response to a file
md_filepath = "c:\\Users\\sssgu\\OneDrive\\Desktop\\Hoohacks\\ScholarMatch\\Backend\\Tests\\Outputs\\results.md"
with open(md_filepath, "w", encoding="utf-8") as f:
    f.write(response.output_text)

print("Results saved to:", md_filepath)

@app.route('/display_md', methods=['GET'])
def display_md():
    md_filepath = "c:\\Users\\sssgu\\OneDrive\\Desktop\\Hoohacks\\ScholarMatch\\Backend\\Tests\\Outputs\\results.md"
    with open(md_filepath, "r", encoding="utf-8") as f:
        md_content = f.read()
    return render_template("results.html", md_content=md_content)


