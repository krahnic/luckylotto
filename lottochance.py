import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from collections import Counter
from math import floor

class LotterySimulator:
    def __init__(self):
        self.history = []
        self.popular_combinations = set()
        self.number_frequency = Counter()

    def generate_lottery_numbers(self):
        return sorted(random.sample(range(1, 50), 6))

    def run_lottery(self):
        numbers = self.generate_lottery_numbers()
        self.history.append(numbers)
        self.update_statistics(numbers)
        return numbers

    def update_statistics(self, numbers):
        self.number_frequency.update(numbers)
        self.popular_combinations.add(tuple(numbers))

    def predict_smart_numbers(self):
        hot_numbers = [num for num, _ in self.number_frequency.most_common(10)]
        cold_numbers = [num for num, _ in self.number_frequency.most_common()[-10:]]
        smart_numbers = []

        while len(smart_numbers) < 6:
            if hot_numbers and random.random() < 0.5:
                number = random.choice(hot_numbers)
            elif cold_numbers:
                number = random.choice(cold_numbers)
            else:
                number = random.randint(1, 49)
            
            if number not in smart_numbers:
                smart_numbers.append(number)

        return sorted(smart_numbers)

    def get_overdue_numbers(self):
        all_numbers = set(range(1, 50))
        recent_numbers = set()
        for draw in self.history[-10:]:
            recent_numbers.update(draw)
        overdue = list(all_numbers - recent_numbers)
        random.shuffle(overdue)
        return overdue

    def get_frequent_numbers(self):
        return [num for num, _ in self.number_frequency.most_common(10)]

    def is_popular_combination(self, numbers):
        return tuple(numbers) in self.popular_combinations

def calculate_prize(correct_count):
    prizes = {
        6: 20000000,
        5: 50000,
        4: 1000,
        3: 10,
        2: 5
    }
    return prizes.get(correct_count, 0)

def compare_results(prediction, actual):
    correct = set(prediction) & set(actual)
    correct_count = len(correct)
    prize = calculate_prize(correct_count)
    return correct_count, prize, sorted(list(correct))

def calculate_time_played(rounds):
    total_days = rounds * 3.5
    years = floor(total_days / 365)
    remaining_days = round(total_days % 365)
    if years > 0:
        return f"{years} year{'s' if years > 1 else ''} and {remaining_days} day{'s' if remaining_days != 1 else ''}"
    else:
        return f"{remaining_days} day{'s' if remaining_days != 1 else ''}"

class LotteryApp:
    def __init__(self, root):
        self.simulator = LotterySimulator()
        self.round_number = 0
        self.total_predictions = 0
        self.money_score = 0
        self.total_winnings = 0
        self.total_winning_predictions = 0
        self.jackpot_wins = 0
        self.five_number_wins = 0
        self.four_number_wins = 0
        self.three_number_wins = 0
        self.two_number_wins = 0

        self.root = root
        self.root.title("Lottery Simulator")
        self.root.geometry("1000x800")  # Set the initial window size

        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add default logo
        self.default_logo_image = Image.open("lottery_logo.png")
        self.default_logo_image = self.default_logo_image.resize((200, 200), Image.LANCZOS)
        self.default_logo_photo = ImageTk.PhotoImage(self.default_logo_image)

        # Add jackpot winner logo
        self.jackpot_winner_logo_image = Image.open("jackpot_winner_logo.png")
        self.jackpot_winner_logo_image = self.jackpot_winner_logo_image.resize((200, 200), Image.LANCZOS)
        self.jackpot_winner_logo_photo = ImageTk.PhotoImage(self.jackpot_winner_logo_image)

        # Add 5-number winner logo
        self.five_number_winner_logo_image = Image.open("five_number_winner_logo.png")
        self.five_number_winner_logo_image = self.five_number_winner_logo_image.resize((200, 200), Image.LANCZOS)
        self.five_number_winner_logo_photo = ImageTk.PhotoImage(self.five_number_winner_logo_image)

        self.logo_label = ttk.Label(self.scrollable_frame, image=self.default_logo_photo)
        self.logo_label.grid(row=0, column=0, columnspan=3)

        self.round_label = ttk.Label(self.scrollable_frame, text="Round: 0")
        self.round_label.grid(row=1, column=0, sticky=tk.W)

        self.predictions_text = tk.Text(self.scrollable_frame, width=50, height=10, wrap=tk.WORD)
        self.predictions_text.grid(row=2, column=0, columnspan=3, pady=5)

        self.actual_numbers_label = ttk.Label(self.scrollable_frame, text="Actual Lottery Numbers: []")
        self.actual_numbers_label.grid(row=3, column=0, sticky=tk.W)

        self.results_text = tk.Text(self.scrollable_frame, width=50, height=10, wrap=tk.WORD)
        self.results_text.grid(row=4, column=0, columnspan=3, pady=5)

        self.money_score_label = tk.Label(self.scrollable_frame, text="Current Money Score: $0", fg="blue", font=("Helvetica", 12, "bold"))
        self.money_score_label.grid(row=5, column=0, columnspan=3, pady=5)

        self.total_winnings_label = tk.Label(self.scrollable_frame, text="Total Winnings: $0", fg="grey", font=("Helvetica", 10))
        self.total_winnings_label.grid(row=6, column=0, columnspan=3)

        self.prize_counts_label = tk.Label(self.scrollable_frame, text="Jackpot Wins: 0 | 5-Number Wins: 0 | 4-Number Wins: 0 | 3-Number Wins: 0 | 2-Number Wins: 0", fg="grey", font=("Helvetica", 10))
        self.prize_counts_label.grid(row=7, column=0, columnspan=3)

        self.time_played_label = tk.Label(self.scrollable_frame, text="", fg="grey", font=("Helvetica", 10))
        self.time_played_label.grid(row=8, column=0, columnspan=3)

        self.play_button = ttk.Button(self.scrollable_frame, text="Play Round", command=self.play_round)
        self.play_button.grid(row=9, column=0, pady=5, sticky=tk.W)

        self.reset_button = ttk.Button(self.scrollable_frame, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=9, column=1, pady=5)

        self.quit_button = ttk.Button(self.scrollable_frame, text="Quit", command=root.quit)
        self.quit_button.grid(row=9, column=2, pady=5, sticky=tk.E)

        self.rounds_entry = ttk.Entry(self.scrollable_frame, width=5)
        self.rounds_entry.grid(row=10, column=0, pady=5, sticky=tk.W)
        self.rounds_entry.insert(0, "1")

        self.play_multiple_button = ttk.Button(self.scrollable_frame, text="Play Multiple Rounds", command=self.play_multiple_rounds)
        self.play_multiple_button.grid(row=10, column=1, pady=5)

        # User numbers frame on the right side
        self.user_numbers_frame = ttk.Frame(self.scrollable_frame)
        self.user_numbers_frame.grid(row=0, column=3, rowspan=17, padx=10, pady=5, sticky="n")

        ttk.Label(self.user_numbers_frame, text="Select Your Numbers", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=5)

        self.user_numbers_vars = []
        for i in range(6):  # Allow up to 6 sets of user numbers
            frame = ttk.LabelFrame(self.user_numbers_frame, text=f"Set {i+1}")
            frame.grid(row=i+1, column=0, padx=5, pady=5)
            vars = [tk.IntVar() for _ in range(49)]
            self.user_numbers_vars.append(vars)
            for j in range(49):
                checkbutton = ttk.Checkbutton(frame, text=str(j+1), variable=vars[j])
                checkbutton.grid(row=j//10, column=j%10)

        self.play_ai_var = tk.BooleanVar(value=True)
        self.play_user_var = tk.BooleanVar(value=False)

        self.play_ai_check = ttk.Checkbutton(self.scrollable_frame, text="Play AI Numbers", variable=self.play_ai_var)
        self.play_ai_check.grid(row=11, column=0, pady=5)

        self.play_user_check = ttk.Checkbutton(self.scrollable_frame, text="Play User Numbers", variable=self.play_user_var)
        self.play_user_check.grid(row=11, column=1, pady=5)

    def update_money_score_color(self):
        if self.money_score < 0:
            self.money_score_label.config(fg="red")
        else:
            self.money_score_label.config(fg="green")

    def update_prize_counts(self):
        self.prize_counts_label.config(
            text=f"Jackpot Wins: {self.jackpot_wins} | 5-Number Wins: {self.five_number_wins} | 4-Number Wins: {self.four_number_wins} | 3-Number Wins: {self.three_number_wins} | 2-Number Wins: {self.two_number_wins}"
        )

    def get_user_numbers(self):
        user_numbers_list = []
        for vars in self.user_numbers_vars:
            user_numbers = [i+1 for i, var in enumerate(vars) if var.get() == 1]
            if user_numbers:
                if len(user_numbers) != 6:
                    messagebox.showerror("Invalid input", "Please select exactly 6 numbers for each set.")
                    return []
                user_numbers_list.append(sorted(user_numbers))
        return user_numbers_list

    def play_round(self):
        self.round_number += 1
        self.round_label.config(text=f"Round: {self.round_number}")

        # Run several lotteries to build up history
        for _ in range(10):
            self.simulator.run_lottery()

        # Generate sets of predictions
        predictions = []
        self.predictions_text.delete(1.0, tk.END)

        if self.play_ai_var.get():
            for i in range(6):
                prediction = self.simulator.predict_smart_numbers()
                while self.simulator.is_popular_combination(prediction) or prediction in predictions:
                    prediction = self.simulator.predict_smart_numbers()
                predictions.append(prediction)
                self.predictions_text.insert(tk.END, f"AI's smart prediction #{i+1}: {prediction}\n")

        if self.play_user_var.get():
            user_numbers_list = self.get_user_numbers()
            if user_numbers_list:
                for user_numbers in user_numbers_list:
                    predictions.append(user_numbers)
                    self.predictions_text.insert(tk.END, f"User's numbers: {user_numbers}\n")

        self.total_predictions += len(predictions)
        self.money_score -= len(predictions) * 3

        actual = self.simulator.run_lottery()
        self.actual_numbers_label.config(text=f"Actual Lottery Numbers: {actual}")

        self.results_text.delete(1.0, tk.END)
        total_correct = 0
        round_winnings = 0
        jackpot_won = False
        five_number_won = False
        for i, prediction in enumerate(predictions, 1):
            correct_count, prize, correct_numbers = compare_results(prediction, actual)
            total_correct += correct_count
            round_winnings += prize
            if prize > 0:
                self.total_winning_predictions += 1
                if correct_count == 6:
                    jackpot_won = True
                    self.jackpot_wins += 1
                elif correct_count == 5:
                    five_number_won = True
                    self.five_number_wins += 1
                elif correct_count == 4:
                    self.four_number_wins += 1
                elif correct_count == 3:
                    self.three_number_wins += 1
                elif correct_count == 2:
                    self.two_number_wins += 1
            
            result_text = f"Prediction #{i}: {correct_count} correct {correct_numbers if correct_numbers else ''}"
            if prize > 0:
                result_text += f" - ${prize}\n"
            else:
                result_text += "\n"
            self.results_text.insert(tk.END, result_text)

        self.money_score += round_winnings
        self.total_winnings += round_winnings

        if jackpot_won:
            self.results_text.insert(tk.END, "\nCongratulations! You've won the jackpot!\n")
            self.logo_label.config(image=self.jackpot_winner_logo_photo)
        elif five_number_won:
            self.results_text.insert(tk.END, "\nCongratulations! You've won the 5-number prize!\n")
            self.logo_label.config(image=self.five_number_winner_logo_photo)

        self.results_text.insert(tk.END, f"\nTotal correct numbers: {total_correct}\n")
        self.results_text.insert(tk.END, f"Total winning predictions: {self.total_winning_predictions}\n")
        self.results_text.insert(tk.END, f"Round winnings: ${round_winnings}\n")

        current_odds = self.total_winning_predictions / self.total_predictions * 100
        time_played = calculate_time_played(self.round_number)

        self.results_text.insert(tk.END, f"\nTotal predictions made: {self.total_predictions}\n")
        self.results_text.insert(tk.END, f"Total winnings: ${self.total_winnings}\n")
        self.results_text.insert(tk.END, f"Current odds of winning: {current_odds:.2f}%\n")
        self.results_text.insert(tk.END, f"Time played: {time_played}\n")

        self.money_score_label.config(text=f"Current Money Score: ${self.money_score}")
        self.update_money_score_color()
        self.total_winnings_label.config(text=f"Total Winnings: ${self.total_winnings}")
        self.time_played_label.config(text=f"Time played: {time_played}")
        self.update_prize_counts()

    def play_multiple_rounds(self):
        try:
            rounds_to_play = int(self.rounds_entry.get())
            for _ in range(rounds_to_play):
                self.play_round()
        except ValueError:
            self.results_text.insert(tk.END, "\nInvalid input! Please enter a valid number.\n")

    def reset_game(self):
        self.round_number = 0
        self.total_predictions = 0
        self.money_score = 0
        self.total_winnings = 0
        self.total_winning_predictions = 0
        self.jackpot_wins = 0
        self.five_number_wins = 0
        self.four_number_wins = 0
        self.three_number_wins = 0
        self.two_number_wins = 0

        self.round_label.config(text="Round: 0")
        self.predictions_text.delete(1.0, tk.END)
        self.actual_numbers_label.config(text="Actual Lottery Numbers: []")
        self.results_text.delete(1.0, tk.END)
        self.money_score_label.config(text="Current Money Score: $0", fg="blue")
        self.total_winnings_label.config(text="Total Winnings: $0")
        self.time_played_label.config(text="")
        self.logo_label.config(image=self.default_logo_photo)
        self.update_prize_counts()

        for vars in self.user_numbers_vars:
            for var in vars:
                var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()