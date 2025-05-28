import requests
import html
from tkinter import *
from tkinter import messagebox
import random
import json

# ---------------------------- CLASSES ------------------------------- #
class QuizLeaderboard:
    def __init__(self):
        default_data = {
            "player": {
                "score": 0
            }
        }
        try:
            with open("leaderboard.json", "r") as file:
                leaderboard_data = json.load(file)
        except FileNotFoundError:
            with open("leaderboard.json", "w") as file:
                json.dump(default_data, file, indent=4)
            with open("leaderboard.json", "r") as file:
                leaderboard_data = json.load(file)
        self.leaderboard_data = leaderboard_data
        self.player_list = list(self.leaderboard_data.keys())

    def add_player_score(self, player, score):
        new_player = {
            player: {
                "score": score
            }
        }
        with open("leaderboard.json", "r") as file:
            data = json.load(file)
        data.update(new_player)
        with open("leaderboard.json", "w") as file:
            json.dump(data, file, indent=4)

class QuizContent:
    def __init__(self):
        self.question_data = {}
        self.get_question_data()
        self.questions = [html.unescape(question["question"]) for question in self.question_data["results"]]
        self.correct_answers = [html.unescape(question["correct_answer"]) for question in self.question_data["results"]]
        self.incorrect_answers = [html.unescape(question["incorrect_answers"]) for question in self.question_data["results"]]
        self.possible_answers = [[self.correct_answers[i]] + self.incorrect_answers[i] for i in range(len(self.incorrect_answers))]
        self.shuffle_possible_answers()

    def get_question_data(self):
        url = "https://opentdb.com/api.php"
        parameters = {
            "amount": 10,
            "type": "multiple",
            "category": 15
        }
        response = requests.get(url, parameters)
        self.question_data = response.json()

    def shuffle_possible_answers(self):
        for answers in self.possible_answers:
            random.shuffle(answers)

class QuizBrain:
    def __init__(self, content: QuizContent):
        self.content = content
        self.question_number = 0
        self.score = 0
        self.current_question = self.content.questions[self.question_number]
        self.current_correct_answer = self.content.correct_answers[self.question_number]
        self.current_possible_answers = self.content.possible_answers[self.question_number]
        self.next_question()

    def still_has_questions(self):
        return self.question_number < len(self.content.questions)

    def next_question(self):
        self.current_question = self.content.questions[self.question_number]
        self.current_correct_answer = self.content.correct_answers[self.question_number]
        self.current_possible_answers = self.content.possible_answers[self.question_number]
        self.question_number += 1

    def check_user_answer(self, answer):
        return answer == self.current_correct_answer

class QuizUI:
    def __init__(self, quiz: QuizBrain, leaderboard: QuizLeaderboard):
        self.quiz = quiz
        self.leaderboard = leaderboard
        self.current_player = ""

        self.window = Tk()
        self.window.title("Trivia Trials")
        self.window.config(padx=20, pady=20)

        self.title_text = Label(text="Welcome to Trivia Trials", font=("San Fransisco", 30), wraplength=250)
        self.title_text.grid(row=0, column=0)

        self.score_text = Label(text=f"Score: {self.quiz.score}", font=("San Fransisco", 15))

        self.leaderboard_player_text = Label(text="PLAYER", font=("San Fransisco", 15))
        self.leaderboard_score_text = Label(text="SCORE", font=("San Fransisco", 15))

        self.canvas = Canvas(width=250, height=250, highlightthickness=0)
        self.question_text = self.canvas.create_text(125, 125, text="Are you ready to start?", font=("San Fransisco", 15), width=230, justify="center")
        self.canvas.grid(row=1, column=0)

        self.start_button = Button(text="Start", font=("San Fransisco", 10), wraplength=250, width=30, command=self.start_func, relief="groove")
        self.start_button.grid(row=2, column=0)

        self.option1_button = Button(text=self.quiz.current_possible_answers[0], font=("San Fransisco", 10), wraplength=250, width=30, command=self.option1_func, relief="groove")
        self.option2_button = Button(text=self.quiz.current_possible_answers[1], font=("San Fransisco", 10), wraplength=250, width=30, command=self.option2_func, relief="groove")
        self.option3_button = Button(text=self.quiz.current_possible_answers[2], font=("San Fransisco", 10), wraplength=250, width=30, command=self.option3_func, relief="groove")
        self.option4_button = Button(text=self.quiz.current_possible_answers[3], font=("San Fransisco", 10), wraplength=250, width=30, command=self.option4_func, relief="groove")

        self.username_text = Label(text=f"Enter Username:", font=("San Fransisco", 15))
        self.username_entry = Entry(width=30)

        self.add_username_button = Button(text="Add", font=("San Fransisco", 10), width=10, command=self.add_username_func, relief="groove")

        self.window.mainloop()

    def update_ui(self):
        self.option1_button["state"] = "normal"
        self.option2_button["state"] = "normal"
        self.option3_button["state"] = "normal"
        self.option4_button["state"] = "normal"
        self.title_text.config(text=f"Question {self.quiz.question_number}")
        self.score_text.config(text=f"Score: {self.quiz.score}")
        self.canvas.itemconfig(self.question_text, text=self.quiz.current_question)
        self.option1_button.config(text=self.quiz.current_possible_answers[0])
        self.option2_button.config(text=self.quiz.current_possible_answers[1])
        self.option3_button.config(text=self.quiz.current_possible_answers[2])
        self.option4_button.config(text=self.quiz.current_possible_answers[3])

    def start_func(self):
        self.start_button.grid_forget()
        self.score_text.grid(row=1, column=0)
        self.canvas.grid(row=2, column=0)
        self.option1_button.grid(row=3, column=0)
        self.option2_button.grid(row=4, column=0)
        self.option3_button.grid(row=5, column=0)
        self.option4_button.grid(row=6, column=0)
        self.update_ui()

    def answer_feedback(self, answer):
        if self.quiz.check_user_answer(answer):
            self.canvas.itemconfig(self.question_text, text=f"Correct")
            self.score_text.config(text=f"Score: {self.quiz.score}")
        else:
            self.canvas.itemconfig(self.question_text, text=f"Incorrect\nThe answer was {self.quiz.current_correct_answer}")
        self.window.after(ms=2000, func=self.update_ui)

    def end_game_ui(self):
        self.title_text.config(text="You Finished")
        self.title_text.grid(row=0, column=0, columnspan=3)
        self.score_text.config(text=f"Final Score: {self.quiz.score}")
        self.score_text.grid(row=1, column=0, columnspan=3)
        self.username_text.grid(row=2, column=0)
        self.username_entry.grid(row=2, column=1)
        self.add_username_button.grid(row=2, column=2)
        self.username_entry.focus()
        self.canvas.grid_forget()
        self.option1_button.grid_forget()
        self.option2_button.grid_forget()
        self.option3_button.grid_forget()
        self.option4_button.grid_forget()

    def option1_func(self):
        self.option1_button["state"] = "disabled"
        self.option2_button["state"] = "disabled"
        self.option3_button["state"] = "disabled"
        self.option4_button["state"] = "disabled"
        user_answer = self.quiz.current_possible_answers[0]
        if self.quiz.check_user_answer(user_answer):
            self.quiz.score += 1
        if self.quiz.still_has_questions():
            self.answer_feedback(user_answer)
            self.quiz.next_question()
        else:
            self.answer_feedback(user_answer)
            self.window.after(2001, self.end_game_ui)

    def option2_func(self):
        self.option1_button["state"] = "disabled"
        self.option2_button["state"] = "disabled"
        self.option3_button["state"] = "disabled"
        self.option4_button["state"] = "disabled"
        user_answer = self.quiz.current_possible_answers[1]
        if self.quiz.check_user_answer(user_answer):
            self.quiz.score += 1
        if self.quiz.still_has_questions():
            self.answer_feedback(user_answer)
            self.quiz.next_question()
        else:
            self.answer_feedback(user_answer)
            self.window.after(2001, self.end_game_ui)

    def option3_func(self):
        self.option1_button["state"] = "disabled"
        self.option2_button["state"] = "disabled"
        self.option3_button["state"] = "disabled"
        self.option4_button["state"] = "disabled"
        user_answer = self.quiz.current_possible_answers[2]
        if self.quiz.check_user_answer(user_answer):
            self.quiz.score += 1
        if self.quiz.still_has_questions():
            self.answer_feedback(user_answer)
            self.quiz.next_question()
        else:
            self.answer_feedback(user_answer)
            self.window.after(2001, self.end_game_ui)

    def option4_func(self):
        self.option1_button["state"] = "disabled"
        self.option2_button["state"] = "disabled"
        self.option3_button["state"] = "disabled"
        self.option4_button["state"] = "disabled"
        user_answer = self.quiz.current_possible_answers[3]
        if self.quiz.check_user_answer(user_answer):
            self.quiz.score += 1
        if self.quiz.still_has_questions():
            self.answer_feedback(user_answer)
            self.quiz.next_question()
        else:
            self.answer_feedback(user_answer)
            self.window.after(2001, self.end_game_ui)

    def add_username_func(self):
        self.current_player = self.username_entry.get()
        if self.current_player == "":
            messagebox.showerror(title="Invalid Input", message="Please do not leave username empty")
        else:
            self.leaderboard.add_player_score(self.current_player, self.quiz.score)
            self.display_leaderboard()

    def display_leaderboard(self):
        player_names = "PLAYER"
        player_scores = "SCORE"
        for player in quiz_leaderboard.player_list:
            if player != "player":
                player_names += f"\n{player}"
                player_scores += f"\n{quiz_leaderboard.leaderboard_data[player]["score"]}"
        player_names += f"\n{self.current_player}"
        player_scores += f"\n{self.quiz.score}"
        self.title_text.config(text="Leaderboard")
        self.leaderboard_player_text.config(text=player_names)
        self.leaderboard_score_text.config(text=player_scores)
        self.leaderboard_player_text.grid(row=1, column=0)
        self.leaderboard_score_text.grid(row=1, column=1)
        self.score_text.grid_forget()
        self.username_text.grid_forget()
        self.username_entry.grid_forget()
        self.add_username_button.grid_forget()

# ---------------------------- MAIN ------------------------------- #
quiz_leaderboard = QuizLeaderboard()
quiz_content = QuizContent()
quiz_brain = QuizBrain(quiz_content)
quiz_ui = QuizUI(quiz_brain, quiz_leaderboard)
