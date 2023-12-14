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

"""snake_case?"""
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
        """Löser spelet med en backtracking-algoritm."""
        if self._place_troll_recursive(0):
            print("En lösning hittades:")
            self.print_board()
        else:
            print("Ingen lösning kunde hittas.")

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

# Huvudprogram
def main():
    try:
        size = int(input("Välj storleken på brädet (minst 4): "))
        if size < 4:
            raise ValueError
    except ValueError:
        print("Ogiltig storlek, använder standardstorleken 4x4.")
        size = 4

    game = TrollGame(size)
    auto_solve = input("Vill du lösa spelet automatiskt? (ja/nej): ").lower()
    if auto_solve == 'ja':
        game.solve_game()
    else:
        game.play_game()

main()
