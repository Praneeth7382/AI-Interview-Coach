from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

print("\n===== AI Interview Coach =====\n")

role = input("Enter job role: ")
experience = input("Enter experience level: ")
skills = input("Enter your skills: ")

prompt = f"""
You are a professional technical interviewer with 10 years of experience.

Generate:

1. Five technical interview questions
2. Five HR questions
3. Sample answers
4. Improvement tips

Candidate details:

Role: {role}
Experience: {experience}
Skills: {skills}

Requirements:

- Questions must match role and skills
- Avoid generic questions
- Keep answers concise
- Use clean headings
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role":"user",
            "content":prompt
        }
    ]
)

print("\n")
print(response.choices[0].message.content)