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


def main():
    message = ''
    while True:
        menu(message)
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


if __name__ == '__main__':
    main()
