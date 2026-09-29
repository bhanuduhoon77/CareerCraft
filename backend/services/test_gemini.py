# from backend.services.gemini_service import analyze_resume


# resume_text = """
# Yash Royal

# Education:
# B.Tech Computer Science

# Skills:
# Java, Python, SQL, FastAPI, LangChain, LangGraph

# Projects:
# Multi-Agent AI Assistant
# Document Q&A Chatbot
# Netflix Data Analytics Dashboard

# Certifications:
# AWS Machine Learning Engineer
# """


# result = analyze_resume(resume_text)

# print("\n========== GEMINI RESPONSE ==========\n")
# print(result)
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={
        "timeout": 120000
    }
)

print(">>> Testing Gemini...")

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Say hello in one sentence."
)

print(">>> Gemini response:")
print(response.text)