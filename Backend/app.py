import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route('/match', methods=['POST'])
def match_scholarships():
    data = request.get_json()  # expects JSON with field values
    gpa = data.get("gpa", "")
    is_citizen = data.get("us_citizen", "")
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
        "Return a JSON array where each element is an object with keys 'title', 'deadline', and 'requirements'."
    )
    
    response = client.responses.create(
        model="gpt-4o",
        tools=[{"type": "web_search_preview"}],
        input=prompt
    )
    
    try:
        scholarships = json.loads(response.output_text)
    except Exception as e:
        scholarships = {"error": "Could not parse GPT response"}
    
    return render_template("results.html", scholarships=scholarships)

if __name__ == '__main__':
    app.run(debug=True)


