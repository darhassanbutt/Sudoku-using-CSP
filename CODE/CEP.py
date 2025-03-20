import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constraint import Problem, AllDifferentConstraint
import random

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 8 Project - Sudoku 9x9")
        self.root.geometry("600x600")
        self.root.configure(bg="black")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='black', foreground='white')
        style.configure('TButton', background='blue', foreground='white')
        style.configure('TLabel', font=('Arial', 16))
        style.configure('Horizontal.TProgressbar', background='blue', troughcolor='black')
        
        self.create_title()
        self.create_grid()
        self.create_buttons()

    def create_title(self):
        title_label = tk.Label(self.root, text="Sudoku using CSP", font=('Arial', 18, 'bold'),fg="#B026FF",bg="black")
        title_label.pack(pady=10)

    def create_grid(self):
        self.grid_frame = tk.Frame(self.root,bg="black")
        self.grid_frame.pack()

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                cell = tk.Entry(
                    self.grid_frame,
                    width=4,
                    font=('Arial', 16),
                    justify='center',
                    bd=2,
                    relief='solid',  # Add a solid border
                    bg = "#ADD8E6",
                    fg = "black"
                )
                cell.grid(row=i, column=j, padx=1, pady=1)
                self.cells[i][j] = cell

                # Add thicker border for 3x3 partitions
                if i % 3 == 0 and i != 0:
                    cell.grid(pady=(10, 2))
                if j % 3 == 0 and j != 0:
                    cell.grid(padx=(10, 2))

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg='black')  # Set background color to black
        button_frame.pack()

        solve_button = tk.Button(
            button_frame,
            text="Solve using AI",
            command=self.solve_sudoku,
            font=('Arial', 14),
            bg='#800080',  # Set button background color to yellow
            fg='white'  # Set button text color to black
        )
        solve_button.pack(side=tk.LEFT, padx=5,pady=15)

        check_button = tk.Button(
            button_frame,
            text="Check",
            command=self.check_solution,
            font=('Arial', 14),
            bg='#800080',  # Set button background color to yellow
            fg='white'  # Set button text color to black
        )
        check_button.pack(side=tk.LEFT, padx=5,pady=15)

        new_game_button = tk.Button(
            button_frame,
            text="New Game",
            command=self.new_game,
            font=('Arial', 14),
            bg='#800080',  # Set button background color to yellow
            fg='white'  # Set button text color to black
        )
        new_game_button.pack(side=tk.LEFT, padx=5,pady=15)

    def initialize_board(self):
        # Initialize the Sudoku board with some values
        initial_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                if initial_board[i][j] != 0:
                    self.cells[i][j].insert(0, str(initial_board[i][j]))

    def new_game(self):
        self.initialize_board()

        # Randomly remove some values to create a puzzle
        for _ in range(20):
            i, j = random.randint(0, 8), random.randint(0, 8)
            self.cells[i][j].delete(0, tk.END)

    def solve_sudoku(self):
        solution = self.check_solution(solving=True)
        if solution:
            for i in range(9):
                for j in range(9):
                    value = solution[0][(i, j)]
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(value))

    def check_solution(self, solving=False):
        # Create a CSP problem
        problem = Problem()

        # Add variables (cells) to the problem
        for i in range(9):
            for j in range(9):
                problem.addVariable((i, j), list(range(1, 10)))

        # Add constraints for rows, columns, and squares
        for i in range(9):
            problem.addConstraint(AllDifferentConstraint(), [(i, j) for j in range(9)])  # Rows
            problem.addConstraint(AllDifferentConstraint(), [(j, i) for j in range(9)])  # Columns

        # Additional constraints for 3x3 subgrids
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                problem.addConstraint(AllDifferentConstraint(), [(i + x, j + y) for x in range(3) for y in range(3)])

        # Set user input as constraints
        for i in range(9):
            for j in range(9):
                value = self.cells[i][j].get()
                if value:
                    problem.addConstraint(lambda var, val=int(value): var == val, [(i, j)])

        # Solve the CSP problem
        solution = problem.getSolutions()

        if not solving:
            if solution:
                messagebox.showinfo("Sudoku Solver", "Solution is correct!")
            else:
                messagebox.showinfo("Sudoku Solver", "Solution is incorrect.")

        return solution

if __name__ == "__main__":
    root = tk.Tk()
    sudoku_game = SudokuGame(root)
    root.mainloop()