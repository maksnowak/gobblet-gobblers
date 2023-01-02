import os
from game import Game
from termcolor import colored


class Interface:
    def __init__(self, game: Game) -> None:
        self.__game = game

    def game(self):
        return self.__game

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

    def pieces(self, player, with_ai):
        if player == 'player_one':
            pieces_list = self.game().player_one_pieces()
        else:
            pieces_list = self.game().player_two_pieces()
        pieces_string = ', '.join([str(piece[1]) for piece in pieces_list])
        if with_ai:
            if player == 'player_one':
                return 'Pionki gracza: ' + pieces_string
            else:
                return 'Pionki komputera: ' + pieces_string
        else:
            if player == 'player_one':
                return 'Pionki pierwszego gracza: ' + pieces_string
            else:
                return 'Pionki drugiego gracza: ' + pieces_string


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
