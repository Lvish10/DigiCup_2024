import tkinter as tk
import random

# Define riddles and their solutions
riddles = [
    {"question":"I am made of tiny shells and help prevent coastal erosion. What am I?" ,  "answer":"sand"},
    {"question": "What is the largest animal in the ocean?", "answer": "blue whale"},
    {"question": "I am known as the 'rainforests of the sea'. What am I?", "answer": "coral reef"},
    {"question": "What marine animal has three hearts?", "answer": "octopus"},
    {"question": "What is the term for a group of dolphins?", "answer": "pod"},
    {"question": "Which sea creature is known for its ink-squirting defense mechanism?", "answer": "squid"},
    {"question": "Which marine animal is the most intelligent?", "answer": "dolphin"},
    {"question": "I have five arms but no legs and I live in the ocean. What am I?", "answer": "starfish"},
]

class OceanPuzzleGame:
    def _init_(self, master):
        self.master = master
        self.master.title("Ocean-themed Puzzle Game")
        self.master.geometry("400x400")
        self.master.configure(bg="#2E8BFF")

        self.score = 0
        self.riddles = random.sample(riddles, len(riddles))
        self.current_riddle_index = 0

        self.title_label = tk.Label(master, text="🐳 Ocean Puzzle Game 🐠", font=("Arial", 20, "bold"), bg="#2E8BFF", fg="white")
        self.title_label.pack(pady=20)

        self.score_label = tk.Label(master, text=f"Score: {self.score}", font=("Arial", 16), bg="#2E8BFF", fg="white")
        self.score_label.pack(pady=10)

        self.riddle_frame = tk.Frame(master, bg="#2E8BFF")
        self.riddle_frame.pack(pady=10)

        self.riddle_label = tk.Label(self.riddle_frame, text="", font=("Arial", 14), bg="#2E8BFF", fg="white")
        self.riddle_label.pack(pady=10)

        self.answer_entry = tk.Entry(self.riddle_frame, font=("Arial", 14))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(master, text="Submit Answer", command=self.submit_answer, font=("Arial", 12), bg="#FFBF00", fg="black")
        self.submit_button.pack(pady=10)

        self.display_next_riddle()

    def display_next_riddle(self):
        if self.current_riddle_index < len(self.riddles):
            riddle = self.riddles[self.current_riddle_index]
            self.riddle_label.config(text=riddle["question"])
            self.answer_entry.delete(0, tk.END)
        else:
            self.show_final_score()

    def update_score_display(self):
        self.score_label.config(text=f"Score: {self.score}")

    def submit_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.riddles[self.current_riddle_index]["answer"].lower()

        if user_answer == correct_answer:
            self.score += 1
        else:
            # Show the correct answer without a message box
            self.riddle_label.config(text=f"Incorrect! The correct answer was: {self.riddles[self.current_riddle_index]['answer']}")

        self.current_riddle_index += 1
        self.update_score_display()
        self.display_next_riddle()

    def show_final_score(self):
        self.riddle_label.config(text="Game Over!")
        self.answer_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        # Update the score label with the final score
        self.score_label.config(text=f"Final Score: {self.score}")

if _name_ == "_main_":
    root = tk.Tk()
    game = OceanPuzzleGame(root)
    root.mainloop()