import customtkinter as ctk
from groq import Groq
from dotenv import load_dotenv
from tkinter import filedialog
from pypdf import PdfReader
import threading
import time
import os
import sys

# -------- PROJECT ROOT --------

current_dir=os.path.dirname(__file__)

project_root=os.path.abspath(
    os.path.join(
        current_dir,
        "..",
        ".."
    )
)

sys.path.append(project_root)

# -------- IMPORTS --------

from database import *
from voice import *
from scoring import *
from pdf_export import *

# -------- API --------

load_dotenv()

client=Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -------- VARIABLES --------

resume_content=""

current_score=0

interview_running=False

remaining_time=120

questions=[]

current_question=0

# -------- GUI --------

ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")

app=ctk.CTk()

app.geometry("1100x800")

app.title(
    "AI Interview Coach V3"
)

# -------- FUNCTIONS --------

def upload_resume():

    global resume_content

    file=filedialog.askopenfilename()

    if file:

        reader=PdfReader(file)

        resume_content=""

        for page in reader.pages:

            text=page.extract_text()

            if text:

                resume_content+=text

        textbox.insert(
            "end",
            "\nResume Uploaded Successfully\n"
        )


def export_pdf():

    content=textbox.get(
        "1.0",
        "end"
    )

    create_pdf(content)

    textbox.insert(
        "end",
        "\nPDF Exported\n"
    )


def show_history():

    history=get_history()

    textbox.delete(
        "1.0",
        "end"
    )

    textbox.insert(
        "end",
        "Interview History\n\n"
    )

    for item in history:

        textbox.insert(
            "end",
            str(item)+"\n"
        )


def update_timer():

    global remaining_time
    global interview_running

    while remaining_time>0 and interview_running:

        timer_label.configure(
            text=f"Time Left : {remaining_time} sec"
        )

        time.sleep(1)

        remaining_time-=1

    interview_running=False

    speak(
        "Interview Complete"
    )

    textbox.insert(
        "end",
        "\nInterview Complete\n"
    )


def generate_questions():

    global questions
    global current_question

    role=role_entry.get()

    experience=experience_entry.get()

    level=difficulty_dropdown.get()

    prompt=f"""

Act as a professional interviewer.

Generate only 5 short interview questions.

Candidate:

Role:{role}

Experience:{experience}

Difficulty:{level}

Resume Details:

{resume_content}

Rules:

- Questions must be short
- Role specific
- Ask practical questions
- Avoid generic questions
- Return only numbered questions

"""

    response=client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role":"user",
                "content":prompt
            }

        ]
    )

    result=response.choices[0].message.content

    questions=result.split("\n")

    current_question=0

    textbox.delete(
        "1.0",
        "end"
    )

    textbox.insert(
        "end",
        result
    )


def start_voice_interview():

    global interview_running
    global remaining_time

    if len(questions)==0:

        textbox.insert(
            "end",
            "\nGenerate questions first\n"
        )

        return

    interview_running=True

    remaining_time=120

    threading.Thread(
        target=update_timer,
        daemon=True
    ).start()

    ask_next_question()


def ask_next_question():

    global current_question

    if current_question>=len(questions):

        return

    question=questions[current_question]

    if len(question.strip())>3:

        textbox.insert(
            "end",
            f"\n\nQuestion:\n{question}\n"
        )

        speak(question)


def submit_answer():

    global current_score
    global current_question

    answer=answer_box.get(
        "1.0",
        "end"
    )

    score=calculate_score(
        answer
    )

    current_score+=score

    textbox.insert(
        "end",
        f"\nScore:{score}\n"
    )

    answer_box.delete(
        "1.0",
        "end"
    )

    current_question+=1

    ask_next_question()


# -------- TITLE --------

title=ctk.CTkLabel(

    app,

    text="AI Interview Coach V3",

    font=("Arial",28,"bold")

)

title.pack(
    pady=10
)

# -------- TOP FRAME --------

top_frame=ctk.CTkFrame(
    app
)

top_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

upload_button=ctk.CTkButton(

    top_frame,

    text="Upload Resume",

    command=upload_resume

)

upload_button.pack(
    side="left",
    padx=20
)

export_button=ctk.CTkButton(

    top_frame,

    text="Export PDF",

    command=export_pdf

)

export_button.pack(
    side="right",
    padx=20
)

# -------- INPUT FRAME --------

input_frame=ctk.CTkFrame(
    app
)

input_frame.pack(
    pady=10
)

role_entry=ctk.CTkEntry(

    input_frame,

    width=200,

    placeholder_text="Job Role"

)

role_entry.pack(
    side="left",
    padx=10
)

experience_entry=ctk.CTkEntry(

    input_frame,

    width=200,

    placeholder_text="Experience"

)

experience_entry.pack(
    side="left",
    padx=10
)

difficulty_dropdown=ctk.CTkOptionMenu(

    input_frame,

    values=[

        "Beginner",
        "Intermediate",
        "Advanced"

    ]
)

difficulty_dropdown.pack(
    side="left",
    padx=10
)

generate_button=ctk.CTkButton(

    input_frame,

    text="Generate Questions",

    command=generate_questions

)

generate_button.pack(
    side="left",
    padx=10
)

# -------- TIMER --------

timer_label=ctk.CTkLabel(

    app,

    text="Time Left : 120 sec",

    font=("Arial",18)

)

timer_label.pack()

# -------- OUTPUT --------

textbox=ctk.CTkTextbox(

    app,

    width=1000,

    height=300

)

textbox.pack(
    pady=10
)

# -------- ANSWERS --------

answer_box=ctk.CTkTextbox(

    app,

    width=1000,

    height=100

)

answer_box.pack(
    pady=10
)

submit_button=ctk.CTkButton(

    app,

    text="Submit Answer",

    command=submit_answer

)

submit_button.pack()

# -------- BOTTOM FRAME --------

bottom_frame=ctk.CTkFrame(
    app
)

bottom_frame.pack(
    fill="x",
    padx=20,
    pady=10
)

voice_button=ctk.CTkButton(

    bottom_frame,

    text="Start Voice Interview",

    command=start_voice_interview

)

voice_button.pack(
    side="left",
    padx=20
)

history_button=ctk.CTkButton(

    bottom_frame,

    text="Interview History",

    command=show_history

)

history_button.pack(
    side="right",
    padx=20
)

app.mainloop()