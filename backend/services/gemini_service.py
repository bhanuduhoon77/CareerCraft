import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured in .env")


client = genai.Client(
    api_key=API_KEY,
    http_options={
        "timeout": 120000
    }
)


def analyze_resume(resume_text: str):

    prompt = f"""
You are an expert resume analyzer.

Analyze the following resume.

Return ONLY valid JSON.
Do not add markdown.
Do not add ```json.
Do not add any explanation before or after the JSON.

Use exactly these fields:

{{
    "name": "",
    "education": [],
    "skills": [],
    "experience": [],
    "projects": [],
    "certifications": [],
    "career_preferences": [],
    "strengths": [],
    "missing_skills": []
}}

Resume:

{resume_text}
"""

    print(">>> Sending resume to Gemini...")

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        print(">>> Gemini response received!")

        return response.text

    except Exception as e:

        print(">>> GEMINI ERROR:", repr(e))

        raise


def generate_assessment_questions(topic: str):

    prompt = f"""
You are an expert technical interviewer.

Create a short skill assessment for the topic:

{topic}

Generate exactly 5 multiple-choice questions.

Return ONLY valid JSON.
Do not add markdown.
Do not add ```json.
Do not add any explanation before or after the JSON.

Use exactly this format:

[
    {{
        "question": "",
        "options": ["", "", "", ""],
        "correct_answer": ""
    }}
]

Questions should test practical understanding, not just definitions.
"""

    print(f">>> Generating assessment questions for: {topic}")

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        print(">>> Assessment questions generated!")

        return response.text

    except Exception as e:

        print(">>> GEMINI ASSESSMENT ERROR:", repr(e))

        raise