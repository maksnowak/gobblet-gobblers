from game import Game
from ui import Interface
import os


def menu(output):
    os.system('clear')
    print(f'''
Witaj w grze Gobblet Gobblers!

1) Gra z drugim graczem
2) Gra z komputerem

0) Wyjdź

{output}
''', end='')


def game(size, ai):
    game = Game(size)
    ui = Interface(game, ai)
    turn = 1
    error_output = ''
    while True:
        print(ui.board())
        print(ui.pieces('player_one'))
        print(ui.pieces('player_two'))
        print(error_output)
        break


def main():
    message = ''
    while True:
        menu(message)
        choice = input('Wybierz jedną z powyższych opcji wpisując jej numer: ')
        if choice == '0':
            os.system('clear')
            break
        elif choice == '1':
            message = ''
            size = input('Podaj rozmiar planszy: ')
            if size.isnumeric() and int(size) > 2:
                os.system('clear')
                game(int(size), False)
                break
            else:
                message = 'Nieprawidłowy rozmiar planszy!'
        elif choice == '2':
            message = ''
        else:
            message = 'Nieprawidłowa opcja!'


if __name__ == '__main__':
    main()
