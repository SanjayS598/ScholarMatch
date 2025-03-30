import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from flask import Flask, request, render_template
from flask_cors import CORS  # enable CORS

# Update the Flask app to use the frontend templates folder
app = Flask(__name__, template_folder="../frontend/templates")
CORS(app)  # enable CORS for all routes

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/search', methods=['POST'])
def search_scholarships():
    # Receive JSON data from form submission
    data = request.get_json()
    
    # Save the form data for debugging purposes
    input_filepath = "c:\\Users\\sssgu\\OneDrive\\Desktop\\Hoohacks\\ScholarMatch\\Backend\\Tests\\Inputs\\form_input.json"
    os.makedirs(os.path.dirname(input_filepath), exist_ok=True)
    with open(input_filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    # Extract form-fields from the received JSON
    gpa = data.get("gpa", "")
    major = data.get("major", "")
    degree = data.get("degree", "")
    demographics = data.get("demographics", "")
    graduation = data.get("graduation", "")
    skills = data.get("skills", "")
    sports = data.get("sports", "")
    citizenship = data.get("citizenship", "")
    income = data.get("income", "")
    gender = data.get("gender", "")
    military_status = data.get("military", "")

    prompt = (
        f"Find 10 scholarships for an applicant with the following details:\n"
        f"GPA: {gpa}\n"
        f"Degree Level: {degree}\n"
        f"Ethnicity: {demographics}\n"
        f"Major: {major}\n"
        f"Graduation: {graduation}\n"
        f"Skills: {skills}\n"
        f"Sports: {sports}\n"
        f"Citizenship: {citizenship}\n"
        f"Annual Income: {income}\n"
        f"Gender: {gender}\n"
        f"Military Status: {military_status}\n\n"
        "For each scholarship, give it a match score with the applicant out of 100, make sure to include the scholarship name, amount, eligibility criteria, deadline, and a brief description"
    )

    response = client.responses.create(
        model="gpt-4o",
        tools=[{"type": "web_search_preview"}],
        input=prompt
    )

    # Save GPT's Markdown response to a file
    md_filepath = "c:\\Users\\sssgu\\OneDrive\\Desktop\\Hoohacks\\ScholarMatch\\Backend\\Tests\\Outputs\\results.md"
    os.makedirs(os.path.dirname(md_filepath), exist_ok=True)
    with open(md_filepath, "w", encoding="utf-8") as f:
        f.write(response.output_text)

    print("Results saved to:", md_filepath)
    
    # Return a JSON response so that the route returns a valid response
    return {"status": "success", "message": "Scholarships generated."}

@app.route('/display_md', methods=['GET'])
def display_md():
    md_filepath = "c:\\Users\\sssgu\\OneDrive\\Desktop\\Hoohacks\\ScholarMatch\\Backend\\Tests\\Outputs\\results.md"
    if not os.path.exists(md_filepath):
        return "Results file not found. Please ensure the GPT process ran successfully."
    with open(md_filepath, "r", encoding="utf-8") as f:
        md_content = f.read()
    return render_template("results.html", md_content=md_content)

if __name__ == '__main__':
    app.run(debug=True)


