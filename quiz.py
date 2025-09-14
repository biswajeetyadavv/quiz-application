import tkinter as tk
from tkinter import messagebox
import json

# Load JSON data
with open("data.json", "r") as file:  # update path if needed
    quiz_data = json.load(file)

# Build questions list from your JSON structure
questions = []
for i, q in enumerate(quiz_data["question"]):
    questions.append({
        "question": q,
        "options": quiz_data["options"][i],
        "answer": quiz_data["options"][i][quiz_data["answer"][i] - 1]  # converting index to actual answer
    })

# Initialize Tkinter
root = tk.Tk()
root.geometry("600x400")
root.title("Quiz Application")

# Colors for better look and feel
bg_color = "#f0f8ff"  # Light blue
question_color = "#4caf50"  # Green
button_color = "#2196f3"  # Blue
font_main = ("Arial", 14)
font_question = ("Arial", 16, "bold")

root.configure(bg=bg_color)

# Global Variables
current_question_index = 0
selected_answer = tk.StringVar()  # Stores the user's selected answer
score = 0

# Function to load a question
def load_question(index):
    global selected_answer

    # Clear previous selection
    selected_answer.set(None)

    # Get the current question
    question = questions[index]
    question_text.set(f"{question['question']}")

    # Update options
    for i, option in enumerate(question["options"]):
        option_buttons[i].config(text=option, value=option)

# Function to handle "Next" button click
def next_question():
    global current_question_index, score

    if not selected_answer.get():
        messagebox.showwarning("Warning", "Please select an answer before proceeding!")
        return

    # Check the answer
    if selected_answer.get() == questions[current_question_index]["answer"]:
        score += 1

    # Move to the next question or end the quiz
    current_question_index += 1
    if current_question_index < len(questions):
        load_question(current_question_index)
    else:
        messagebox.showinfo("Quiz Completed", f"Your score is {score}/{len(questions)}")
        root.quit()  # Close the application after completion

# UI Components
question_text = tk.StringVar()

# Display Question Label
question_label = tk.Label(
    root, textvariable=question_text, font=font_question,
    fg=question_color, bg=bg_color, wraplength=500, anchor="w"
)
question_label.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky="w")

# Display Options as Radio Buttons
option_buttons = []
for i in range(4):  # Assuming 4 options per question
    rb = tk.Radiobutton(
        root, text="", variable=selected_answer, value="", font=font_main,
        bg=bg_color, anchor="w", width=40, justify="left", fg="#000"
    )
    rb.grid(row=i + 1, column=0, columnspan=2, padx=20, pady=5, sticky="w")
    option_buttons.append(rb)

# "Next" Button
next_button = tk.Button(
    root, text="Next", command=next_question, bg=button_color,
    fg="white", font=font_main, width=12
)
next_button.grid(row=6, column=0, columnspan=2, pady=20)

# Load the first question
load_question(current_question_index)

# Run the application
root.mainloop()
