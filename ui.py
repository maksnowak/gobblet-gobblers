import os
from game import Game
from termcolor import colored


class Interface:
    def __init__(self, game: Game, ai: bool) -> None:
        self.__game = game
        self.__ai = ai

    def game(self):
        return self.__game

    def ai(self):
        return self.__ai

    def board(self):
        string = '----' * self.game().size() + '-\n'
        for row in self.game().board():
            for cell in row:
                try:
                    if cell[-1][0] == 'player_one':
                        color = 'red'
                    elif cell[-1][0] == 'player_two':
                        color = 'blue'
                    piece = colored(cell[-1][1], color)
                except IndexError:
                    piece = ' '
                string += f'| {piece} '
            string += '|\n' + '----' * self.game().size() + '-\n'
        return string

    def pieces(self, player):
        if player == 'player_one':
            pieces_list = self.game().player_one_pieces()
        else:
            pieces_list = self.game().player_two_pieces()
        pieces_string = ', '.join([str(piece[1]) for piece in pieces_list])
        if self.ai():
            if player == 'player_one':
                return 'Pionki gracza: ' + colored(pieces_string, 'red')
            else:
                return 'Pionki komputera: ' + colored(pieces_string, 'blue')
        else:
            if player == 'player_one':
                return 'Pionki pierwszego gracza: ' + colored(pieces_string, 'red')
            else:
                return 'Pionki drugiego gracza: ' + colored(pieces_string, 'blue')

    def winner(self):
        result = self.game().check_for_win()
        if result is None:
            return
        elif result == 'player_one' and self.ai():
            return 'Wygrana: Gracz'
        elif result == 'player_one' and not self.ai():
            return 'Wygrana: Gracz 1'
        elif result == 'player_two' and self.ai():
            return 'Wygrana: Komputer'
        elif result == 'player_two' and not self.ai():
            return 'Wygrana: Gracz 2'
        else:
            return 'Remis'


if __name__ == '__main__':
    message = ''
    while True:
        os.system('clear')
        print(f'''
Witaj w grze Gobblet Gobblers!

1) Gra z drugim graczem
2) Gra z komputerem

0) Wyjdź

{message}
''', end='')
        choice = input('Wybierz jedną z powyższych opcji wpisując jej numer... ')
        if choice == '0':
            os.system('clear')
            break
        elif choice == '1':
            message = ''
        elif choice == '2':
            message = ''
        else:
            message = 'Nieprawidłowa opcja!'
