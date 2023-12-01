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
        """Huvudfunktion för att spela Trollspelet."""
        import time

        start_time = time.time()
        print("Välkommen till Trollspelet! Försök placera ett troll på varje rad och kolumn utan att bryta mot reglerna.")
        self.print_board()

        for _ in range(self.size):
            valid_move = False
            while not valid_move:
                try:
                    row = int(input(f"Välj rad (0 till {self.size-1}): "))
                    col = int(input(f"Välj kolumn (0 till {self.size-1}): "))
                    valid_move = self.place_troll(row, col)
                    if not valid_move:
                        print("Ogiltigt drag, försök igen.")
                    else:
                        self.print_board()
                except ValueError:
                    print("Ogiltigt inmatningsformat, försök igen.")

        end_time = time.time()
        total_time = self.measure_time(start_time, end_time)
        print(f"Grattis! Du löste spelet på {total_time:.2f} sekunder.")
        self.save_to_highscore(total_time, self.size)

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
    game.play_game()

main()
