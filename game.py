from copy import deepcopy  # necessary for copying nested lists


class PieceUnavailableError(Exception):
    '''Raised when the players does not have the piece'''
    pass


class NotOnBoardError(Exception):
    '''Raised when the piece to be moved is not on the board'''
    pass


class CantCoverPieceError(Exception):
    '''Raised when the piece cannot be moved because another piece is on the same position and it cannot be covered'''
    pass


class Game:
    def __init__(self, size) -> None:
        '''Takes in the board's size and generates a board with dimensions n by n, where n is the given size, two sets of pieces consisting of two pieces of each size and an empty list of recent board layouts'''
        self.__board = []
        # generating the board
        for i in range(size):
            self.__board.append([])
            for _ in range(size):
                self.__board[i].append([])
        self.__player_one = []
        self.__player_two = []
        # creating sets of pieces
        for i in range(size):
            self.__player_one.extend([('player_one', i + 1)] * 2)
            self.__player_two.extend([('player_two', i + 1)] * 2)
        self.__recent_boards = []

    def board(self):
        '''Returns the board with all the pieces on it'''
        return self.__board

    def set_board(self, new_board):
        '''Sets the board's layout with a given one'''
        self.__board = new_board

    def player_one_pieces(self):
        '''Returns the first player's pieces'''
        return self.__player_one

    def set_player_one_pieces(self, new_pieces):
        '''Sets the first player's pieces with a given set'''
        self.__player_one = new_pieces

    def player_two_pieces(self):
        '''Returns the second player's pieces'''
        return self.__player_two

    def set_player_two_pieces(self, new_pieces):
        '''Sets the second player's pieces with a given set'''
        self.__player_two = new_pieces

    def recent_boards(self):
        '''Returns the list of up to 9 recent boards'''
        return self.__recent_boards

    def update_recent_boards(self):
        '''Updates the list of recent boards by adding the current layout to the end of the list. If the list already consists of 9 positions, removes the first element'''
        current_board = deepcopy(self.board())
        boards = deepcopy(self.recent_boards())
        if len(boards) == 9:
            boards.pop(0)
        boards.append(current_board)
        self.__recent_boards = boards

    def move(self, player, size, previous_position, new_position):
        '''Makes a move. Takes in the player who makes the move, the size of a piece to be moved, a tuple with the previous (current) coordinates (or None if the piece will be placed on the board for the first time) and a tuple with the new coordinates. The tuples consist of the x coordinate being the first element and the y coordinate - the second one'''
        # aliasing the pieces' methods in order to avoid repeating the code
        if player == 'player_one':
            player_pieces = self.player_one_pieces
            set_player_pieces = self.set_player_one_pieces
        else:
            player_pieces = self.player_two_pieces
            set_player_pieces = self.set_player_two_pieces
        # checking if player has the piece
        if (player, size) not in player_pieces() and previous_position is None:
            raise PieceUnavailableError('This piece is not available!')
        if previous_position is not None:
            # checking if the piece is on board
            try:
                # when there is a piece at the given coordinates but it is not the same
                if self.board()[previous_position[1] - 1][previous_position[0] - 1][-1] != (player, size):
                    raise NotOnBoardError('This piece is not on the board!')
            # when there is not any piece
            except IndexError:
                raise NotOnBoardError('This piece is not on the board!')
            # TODO get rid of except: pass
            try:
                # checking if there is a piece which cannot be covered
                if size <= self.board()[new_position[1] - 1][new_position[0] - 1][-1][1]:
                    raise CantCoverPieceError('The piece you are trying to cover is larger than your piece!')
            except IndexError:
                pass
        # adding a new piece
        if previous_position is None:
            new_board = deepcopy(self.board())
            new_player_pieces = deepcopy(player_pieces())
            # adding the piece to the end of the list with all the pieces at the given coordinates
            new_board[new_position[1] - 1][new_position[0] - 1].append((player, size))
            new_player_pieces.remove((player, size))
            self.set_board(new_board)
            set_player_pieces(new_player_pieces)
        # moving a piece from the board
        else:
            new_board = deepcopy(self.board())
            new_player_pieces = deepcopy(player_pieces())
            # adding the piece to the end of the list with all the pieces at the given coordinates
            new_board[new_position[1] - 1][new_position[0] - 1].append((player, size))
            new_board[previous_position[1] - 1][previous_position[0] - 1].pop()
            self.set_board(new_board)
            set_player_pieces(new_player_pieces)
        # adding the updated board to the list of recent boards
        self.update_recent_boards()

    def check_for_win(self):
        '''Checks if any player has already won the game, there is a draw (either by repetition or both players having n pieces in row at the same time) or if the game has not been settled yet'''
        possible_winners = []  # necessary for checking a situation where uncovering a piece creates a row for both players
        top_layer = []  # visible pieces on the board only
        # populating the top_layer with pieces (or an empty string if there is none)
        for row in self.board():
            new_row = []
            for cell in row:
                try:
                    new_row.append(cell[-1])
                except IndexError:
                    new_row.append(('',))
            top_layer.append(new_row)
        # checking rows
        for row in top_layer:
            row_pieces = []
            for cell in row:
                row_pieces.append(cell[0])
            # checking if there are only one player's pieces
            if len(set(row_pieces)) == 1 and set(row_pieces) != {''}:
                possible_winners.append(row_pieces[0])
        # checking columns
        for i in range(len(top_layer)):
            column_pieces = []
            for j in range(len(top_layer)):
                column_pieces.append(top_layer[j][i][0])
            # checking if there are only one player's pieces
            if len(set(column_pieces)) == 1 and set(column_pieces) != {''}:
                possible_winners.append(column_pieces[0])
        # checking left diagonal
        left_diagonal_pieces = []
        for i in range(len(top_layer)):
            left_diagonal_pieces.append(top_layer[i][i][0])
        # checking if there are only one player's pieces
        if len(set(left_diagonal_pieces)) == 1 and set(left_diagonal_pieces) != {''}:
            possible_winners.append(left_diagonal_pieces[0])
        # checking right diagonal
        right_diagonal_pieces = []
        for i in range(len(top_layer)):
            right_diagonal_pieces.append(top_layer[i][-1 - i][0])
        # checking if there are only one player's pieces
        if len(set(right_diagonal_pieces)) == 1 and set(right_diagonal_pieces) != {''}:
            possible_winners.append(right_diagonal_pieces[0])
        # checking for draw by repetition
        for board in self.recent_boards():
            if self.recent_boards().count(board) == 3:
                return 'Draw'
        # checking for draw or win
        if len(possible_winners) == 0:
            return None
        elif len(possible_winners) == 1:
            return possible_winners[0]
        else:
            return 'Draw'
