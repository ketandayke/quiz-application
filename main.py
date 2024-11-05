import tkinter as tk
from tkinter import messagebox
import random
from fetch_questions import fetch_questions, load_cached_questions

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("600x400")
        self.root.config(bg="#f0f8ff")  # Light blue background

        # Load questions
        questions_data = fetch_questions(amount=10, category=18, difficulty='easy')
        if not questions_data:
            questions_data = load_cached_questions()

        if not questions_data:
            messagebox.showerror("Error", "No questions available. Please check your internet connection.")
            root.destroy()
            return

        self.questions = self.process_questions(questions_data)
        self.current_question = 0
        self.score = 0

        # UI Elements
        self.question_label = tk.Label(root, wraplength=500, font=("Arial", 16, "bold"), bg="#f0f8ff", justify="center")
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(root, font=("Arial", 12), bg="#add8e6", fg="black", width=20, command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        self.next_button = tk.Button(root, text="Next Question", command=self.next_question, font=("Arial", 12), bg="#4682b4", fg="white")
        self.next_button.pack(pady=20)

        self.result_label = tk.Label(root, font=("Arial", 14, "bold"), bg="#f0f8ff")
        self.result_label.pack(pady=20)

        self.load_question()

    def process_questions(self, questions_data):
        questions = []
        for item in questions_data:
            question = item['question']
            correct_answer = item['correct_answer']
            options = item['incorrect_answers'] + [correct_answer]
            random.shuffle(options)
            questions.append({
                "question": question,
                "options": options,
                "correct_answer": correct_answer
            })
        return questions

    def load_question(self):
        question_data = self.questions[self.current_question]
        self.question_label.config(text=question_data['question'])
        for i, option in enumerate(question_data['options']):
            self.option_buttons[i].config(text=option)

    def check_answer(self, selected_index):
        question_data = self.questions[self.current_question]
        if self.option_buttons[selected_index]['text'] == question_data['correct_answer']:
            self.score += 1
        self.next_question()

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        self.question_label.pack_forget()
        for btn in self.option_buttons:
            btn.pack_forget()
        self.next_button.pack_forget()
        self.result_label.config(text=f"Your score: {self.score}/{len(self.questions)}")
        messagebox.showinfo("Quiz Complete", f"Final Score: {self.score}/{len(self.questions)}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
