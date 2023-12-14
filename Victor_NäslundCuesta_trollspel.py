# Uppgift: 105, Arga Troll
# Namn: Victor Näslund Cuesta
# Datum: 26/11-2023
# Kurskod: DD100N

# Trollspelet går ut på att spelaren ska placera ut arga troll på ett fyrkantigt bräde.
# Trollen ska inte befinna sig på samma rad, kolumn eller diagonal som ett annat troll

# Datastrukturer:
# En klass som innehåller allt som behövs för att spela trollspelet.
# - En matris/board för att representera spelbrädet.
# - En lista för att spara highscores.

import tkinter as tk
from tkinter import messagebox, PhotoImage
import time

class TrollGame:
    def __init__(self, size):
        """Skapar ett nytt trollspel med angiven storlek."""
        self.size = size
        self.board = [['_' for _ in range(size)] for _ in range(size)]
        self.last_move = None

    def print_board(self):
        """Skriver ut aktuellt spelbräde."""
        for row in self.board:
            print(' '.join(row))
        print()

    def place_troll(self, row, col):
        """Placerar ett troll på angiven position om det är tillåtet."""
        if self.is_valid_move(row, col):
            self.board[row][col] = '*'
            self.last_move = (row, col)
            return True
        return False

    def is_valid_move(self, row, col):
        """Kontrollerar om ett drag är tillåtet enligt spelets regler."""
        for i in range(self.size):
            if self.board[row][i] == '*' or self.board[i][col] == '*':
                return False

        """Kontrollera diagonaler, går igenom alla rutor på brädet och
        jämför om distansen till en '*' i x och y-led är lika stor"""
        for i in range(self.size):
            for j in range(self.size):
                if abs(row - i) == abs(col - j) and self.board[i][j] == '*':
                    return False

        return True

    def undo_last_move(self):
        """Ångrar det senaste draget."""
        if self.last_move:
            row, col = self.last_move
            self.board[row][col] = '_'
            self.last_move = None
            return True
        return False

    def measure_time(self, start_time, end_time):
        """Mäter tiden det tar för spelaren att lösa spelet."""
        return end_time - start_time

    def save_to_highscore(self, time, size):
        """Sparar tid och storlek i highscore-listan och skriver till filen."""
        with open("highscores.txt", "a") as file:
            file.write(f"{size}x{size} - {time:.2f} sekunder\n")

    def play_game(self):
        import time

        start_time = time.time()
        print("Välkommen till Trollspelet! Försök placera ett troll på varje rad och kolumn utan att bryta mot reglerna.")
        self.print_board()

        placed_trolls = 0
        while placed_trolls < self.size:
            try:
                user_input = input("Skriv 'undo' för att ångra senaste draget, 'ge upp' för att avsluta, eller välj rad (1 till {}): ".format(self.size))

                if user_input.lower() == 'undo':
                    if self.undo_last_move():
                        print("Senaste draget ångrat.")
                        placed_trolls -= 1
                    else:
                        print("Inget att ångra.")
                elif user_input.lower() == 'ge upp':
                    print("Du har gett upp spelet.")
                    break
                else:
                    row = int(user_input)
                    col = int(input("Välj kolumn (1 till {}): ".format(self.size)))
                    if self.place_troll(row - 1, col - 1):
                        print("Troll placerat.")
                        placed_trolls += 1
                        self.print_board()
                    else:
                        print("Ogiltigt drag, försök igen.")
            except ValueError:
                print("Ogiltigt inmatningsformat, försök igen.")

        if placed_trolls < self.size:
            print("Spelet avslutat utan att lösa det helt.")
        else:
            end_time = time.time()
            total_time = self.measure_time(start_time, end_time)
            print("Grattis! Du löste spelet på {:.2f} sekunder.".format(total_time))
            self.save_to_highscore(total_time, self.size)

    def solve_game(self):
        return self._place_troll_recursive(0)

    def _place_troll_recursive(self, row):
        """En rekursiv hjälpmetod som försöker placera trollen."""
        if row == self.size:
            return True  # Alla troll är placerade

        for col in range(self.size):
            if self.is_valid_move(row, col):
                self.board[row][col] = '*'  # Placera ett troll
                if self._place_troll_recursive(row + 1):
                    return True  # Gå vidare till nästa rad
                self.board[row][col] = '_'  # Ångra placering och prova nästa kolumn

        return False  # Ingen placering fungerade för denna rad

class TrollGameGUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Troll Game")
        self.empty_img = PhotoImage(file='empty.png')  # Sökväg till din tomma bild
        self.troll_img = PhotoImage(file='troll.png')  # Sökväg till din trollbild
        self.buttons = [[None for _ in range(game.size)] for _ in range(game.size)]
        self.create_board()
        self.create_control_buttons()
        self.start_time = time.time()

    def create_board(self):
        for row in range(self.game.size):
            for col in range(self.game.size):
                button = tk.Button(self.root, image=self.empty_img, command=lambda r=row, c=col: self.place_troll(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def update_board(self):
        for row in range(self.game.size):
            for col in range(self.game.size):
                if self.game.board[row][col] == '*':
                    self.buttons[row][col].config(image=self.troll_img)
                else:
                    self.buttons[row][col].config(image=self.empty_img)

    def create_control_buttons(self):
        self.control_button = tk.Button(self.root, text='Lös spelet', command=self.solve_game)
        self.control_button.grid(row=self.game.size, column=0, columnspan=self.game.size, sticky='ew')

    def place_troll(self, row, col):
        if self.game.is_valid_move(row, col):
            self.game.place_troll(row, col)
            self.update_board()
            self.control_button.config(text='Ångra', command=self.undo_last_move)
            if self.check_game_solved():
                self.end_game()

    def solve_game(self):
        if self.game.solve_game():
            self.update_board()
            self.control_button.config(text="Spelet löst av algoritmen", state='disabled')
            self.root.after(5000, self.root.destroy)  # Väntar 5 sekunder innan fönstret stängs
        else:
            print("Ingen lösning kunde hittas.")

    def undo_last_move(self):
        if self.game.undo_last_move():
            self.update_board()

    def end_game(self):
        end_time = time.time()
        total_time = end_time - self.start_time
        print(f"Grattis! Du löste spelet på {total_time:.2f} sekunder.")
        self.game.save_to_highscore(total_time, self.game.size)
        self.root.destroy()

    def check_game_solved(self):
        return all('*' in row for row in self.game.board)

    def run(self):
        self.root.mainloop()

def get_board_size():
    while True:
        try:
            size = int(input("Välj storleken på brädet (minst 4): "))
            if size >= 4:
                return size
            else:
                print("Storleken måste vara minst 4.")
        except ValueError:
            print("Ange en giltig heltalsstorlek.")

# Huvudfunktion för att köra GUI-versionen av spelet
def main():
    size = get_board_size()
    game = TrollGame(size)
    gui = TrollGameGUI(game)
    gui.run()


main()
