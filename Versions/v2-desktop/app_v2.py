import customtkinter as ctk
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x700")
app.title("AI Interview Coach")


title = ctk.CTkLabel(
    app,
    text="AI Interview Coach",
    font=("Arial",28,"bold")
)
title.pack(pady=15)


role_entry = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Enter Job Role"
)
role_entry.pack(pady=10)


experience_entry = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Enter Experience Level"
)
experience_entry.pack(pady=10)


skills_entry = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Enter Skills"
)
skills_entry.pack(pady=10)


textbox = ctk.CTkTextbox(
    app,
    width=800,
    height=350
)
textbox.pack(pady=20)


def generate_questions():

    role = role_entry.get()
    experience = experience_entry.get()
    skills = skills_entry.get()

    prompt = f"""
    You are a professional interviewer with 10 years experience.

    Generate:

    1. Five technical questions
    2. Three HR questions
    3. Sample answers
    4. Improvement tips

    Candidate details:

    Role: {role}
    Experience: {experience}
    Skills: {skills}

    Requirements:
    - Match role and skills
    - Avoid generic questions
    - Use headings
    """

    textbox.delete("1.0","end")

    textbox.insert(
        "end",
        "Generating...\n\n"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    result = response.choices[0].message.content

    textbox.delete("1.0","end")

    textbox.insert(
        "end",
        result
    )


button = ctk.CTkButton(
    app,
    text="Generate Interview Questions",
    command=generate_questions
)

button.pack(pady=10)

app.mainloop()