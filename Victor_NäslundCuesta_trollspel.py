# Uppgift: 105, Arga Troll
# Namn: Victor Näslund Cuesta
# Datum: 26/11-2023
# Kurskod: DD100N

# Trollspelet går ut på att spelaren ska placera ut arga troll på ett fyrkantigt bräde.
# Trollen ska inte befinna sig på samma rad, kolumn eller diagonal som ett annat troll

import tkinter as tk
from tkinter import messagebox, PhotoImage
import time

class troll_game:
    def __init__(self, size):
        """Skapar ett nytt trollspel med angiven storlek (size)"""
        self.size = size
        self.board = [['_' for _ in range(size)] for _ in range(size)]
        self.last_move = None

    def print_board(self):
        """Skriver ut aktuellt spelbräde."""
        for row in self.board:
            print(' '.join(row))
        print()

    def place_troll(self, row, col):
        """Placerar ett troll på angiven position om det är tillåtet
        utifrån inparametrarna som är raden och kolumnen.
        Metoden returnerar true om trollet placerades, annars false"""
        if self.is_valid_move(row, col):
            self.board[row][col] = '*'
            self.last_move = (row, col)
            return True
        return False

    def is_valid_move(self, row, col):
        """Kontrollerar om ett drag är tillåtet enligt spelets regler
        utifrån inparametrarna som är raden och kolumnen.
        Metoden returnerar true om trollet kan placeras, annars false"""
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
        """Ångrar det senaste draget.
        Metoden returnerar true om draget ångrades, annars false"""
        if self.last_move:
            row, col = self.last_move
            self.board[row][col] = '_'
            self.last_move = None
            return True
        return False

    def measure_time(self, start_time, end_time):
        """Mäter tiden det tar för spelaren att lösa spelet
        mha inparametrarna som är starttid och sluttid.
        Returnerar tiden"""
        return end_time - start_time

    def save_to_highscore(self, time, size):
        """Sparar tid och storlek i highscore-listan och skriver till filen.
        Time är tiden det tog att klara spelet för användaren och size är
        hur stort brädet var"""
        with open("highscores.txt", "a") as file:
            file.write(f"{size}x{size} - {time:.2f} sekunder\n")

    def play_game(self):
        """Huvudlogiken för att spela spelet utan GUI. 
        Alltså används inte denna metod i denna version av spelet"""
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
        """Returnerar true om backtracking algoritmen hittade en lösning, annars false"""
        return self._place_troll_recursive(0)

    def _place_troll_recursive(self, row):
        """En rekursiv backtracking algoritm som försöker placera alla trollen.
        inparametern row är vilken rad algoritmen befinner sig på (börjar alltid på 0)"""
        if row == self.size:
            return True  # Alla troll är placerade

        for col in range(self.size):
            if self.is_valid_move(row, col):
                self.board[row][col] = '*'  # Placera ett troll
                if self._place_troll_recursive(row + 1):
                    return True  # Gå vidare till nästa rad
                self.board[row][col] = '_'  # Ångra placering och prova nästa kolumn

        return False  # Ingen placering fungerade för denna rad

class troll_game_gui:
    def __init__(self, game):
        """Initierar GUI-klassen för trollspelet. 
        Använder sig av en instans av troll_game klassen (inparametern game)
        för all funktionalitet förutom det grafiska"""
        self.game = game
        self.root = tk.Tk()
        self.root.title("Trollspelet")
        self.empty_img = PhotoImage(file='empty.png')
        self.troll_img = PhotoImage(file='troll.png')
        self.buttons = [[None for _ in range(game.size)] for _ in range(game.size)]
        self.create_board()
        self.create_control_buttons()
        self.start_time = time.time()

    def create_board(self):
        """Skapar ett bräde av knappar i GUI:t."""
        for row in range(self.game.size):
            for col in range(self.game.size):
                button = tk.Button(self.root, image=self.empty_img, command=lambda r=row, c=col: self.place_troll(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def update_board(self):
        """Uppdaterar brädet i GUI:t för att reflektera spelets nuvarande tillstånd."""
        for row in range(self.game.size):
            for col in range(self.game.size):
                if self.game.board[row][col] == '*':
                    self.buttons[row][col].config(image=self.troll_img)
                else:
                    self.buttons[row][col].config(image=self.empty_img) # Måste också uppdateras pga undo

    def create_control_buttons(self):
        """Skapar kontrollknappar för GUI:t."""
        self.control_button = tk.Button(self.root, text='Lös spelet', command=self.solve_game)
        self.control_button.grid(row=self.game.size, column=0, columnspan=self.game.size, sticky='ew')

    def place_troll(self, row, col):
        """Hanterar logiken för att placera ett troll på brädet.
        row och col är koordinaterna för positionen där trollet ska placeras"""
        if self.game.is_valid_move(row, col):
            self.game.place_troll(row, col)
            self.update_board()
            self.control_button.config(text='Ångra', command=self.undo_last_move)
            if self.check_game_solved():
                self.end_game()

    def solve_game(self):
        """Använder algoritmen från troll_game för att försöka lösa spelet automatiskt."""
        if self.game.solve_game():
            self.update_board()
            self.control_button.config(text="Spelet löst av algoritmen", state='disabled')
            self.root.after(5000, self.root.destroy)  # Väntar 5 sekunder innan fönstret stängs
        else:
            print("Ingen lösning kunde hittas.")

    def undo_last_move(self):
        """Ångrar det senaste draget gjort av spelaren."""
        if self.game.undo_last_move():
            self.update_board()

    def end_game(self):
        """Avslutar spelet och sparar resultatet i highscore-filen."""
        end_time = time.time()
        total_time = end_time - self.start_time
        print(f"Grattis! Du löste spelet på {total_time:.2f} sekunder.")
        self.game.save_to_highscore(total_time, self.game.size)
        self.root.destroy()

    def check_game_solved(self):
        """Kontrollerar om spelet är löst.
        Returnerar true om spelet är löst, annars false"""
        return all('*' in row for row in self.game.board)

    def run(self):
        """Startar huvudloopen för GUI:t."""
        self.root.mainloop()

def get_board_size():
    """Läser spelets storlek från användaren,
    returnerar storleken"""
    while True:
        try:
            size = int(input("Välj storleken på brädet (minimum 4) (max 10 rekommenderas men beror på skärmstorlek): "))
            if size >= 4:
                return size
            else:
                print("Storleken måste vara minst 4.")
        except ValueError:
            print("Ange en giltig heltalsstorlek.")

def print_game_instructions():
    """Skriver ut spelets instruktioner"""
    print("Välkommen till Trollspelet")
    print("Reglerna för spelet är ganska enkla. För att vinna bör du placera:")
    print("-Ett troll per rad.")
    print("-Ett troll per kolumn.")
    print("-Inga troll får finnas på samma diagonal.")

# Huvudfunktion för att köra GUI-versionen av spelet
def main():
    print_game_instructions()
    size = get_board_size()
    game = troll_game(size)
    gui = troll_game_gui(game)
    gui.run()


main()
