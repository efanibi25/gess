# Author: Tobi Fanibi
# Date:06/04/2020
# Description: Includes methods and objects needed to run the game of Gess
# Print the board when needed. Represents the players pieces using bitboards.


"""
Note: 1000 equals=8, 1 is index as first char for string indexing.
However on the board 1 is actually the 4 positon, since we count from the bottom

1 is a piece, and 0 represents a blank spot
"""


def quickpow(exp):
    """
    Use bitwise to calculate exponents of 2
    """
    if exp == 0:
        return 1
    if exp == 1:
        return 2
    if exp > 1:
        return 1 << exp


def converttobinary(input):
    """
    converts int to binary string, removes '1b' that python adds to bin command
    """
    return bin(input)[2:].zfill(400)


class movement:
    """
    This object returns information about a specific movement between two location. Used within the gessgame class
    """

    def __init__(self):
        """
        Creates a movement object
        """
        self._direction = ""
        self._number_of_moves = 0
        self._step = 0

    def movenentor(self, startlocation, endlocation, maxlist):
        """
        Checks if move is valid between two points
        """
        # nw,n,ne,w,e,sw,s,se

        movementlist = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        change = startlocation - endlocation

        if change > 0 and change < 18:
            e = change
            self._direction = "e"
            movementlist[4] = e
            i = 4

        elif change < 0 and change > -18:
            change = change * -1
            self._direction = "w"
            w = change
            movementlist[3] = w
            i = 3

        elif change >= 20 and change % 20 == 0:
            s = int(change / 20)
            self._direction = "s"
            movementlist[6] = s
            i = 6

        elif change <= -20 and change % 20 == 0:
            change = change * -1
            self._direction = "n"
            n = int(change / 20)
            movementlist[1] = n
            i = 1

        elif change > 0 and change % 21 == 0:
            se = int(change / 21)
            self._direction = "se"
            movementlist[7] = se
            i = 7


        elif change < 0 and change % 21 == 0:
            change = change * -1
            self._direction = "nw"
            nw = int(change / 21)
            movementlist[0] = nw
            i = 0


        elif change < 0 and change % 19 == 0:
            change = change * -1
            self._direction = "ne"
            ne = int(change / 19)
            movementlist[2] = ne
            i = 2

        elif change > 0 and change % 19 == 0:
            sw = int(change / 19)
            self._direction = "sw"
            movementlist[5] = sw
            i = 5

        else:
            return False

        # check if max are okay
        if movementlist[i] > maxlist[i]:
            return False
        # only called if movement is allowed, then we can calculate more information
        self.setmovement(self._direction, change)
        return True

    def setmovement(self, direction, change):
        """
        Converts a two dimension grid movement into a one dimension grid movement.
        By setting steps per movement, and total number of movements.
        """
        if direction == 'w':
            self._step = 1
        elif direction == 'e':
            self._step = 1
        elif direction == 'n':
            self._step = 20

        elif direction == 's':
            self._step = 20
        elif direction == 'nw':
            self._step = 21

        elif direction == 'ne':
            self._step = 19
        elif direction == 'sw':
            self._step = 19

        elif direction == 'se':
            self._step = 21

        toomax = 1
        while toomax <= change:
            self._number_of_moves = self._number_of_moves + 1
            toomax = toomax + self._step

        if self._direction == 's' or self._direction == 's' \
                or self._direction == 'sw' or self._direction == 'se' \
                or self._direction == 'e':
            self._step = self._step * -1

    def get_number_of_moves(self):
        """
          Returns number_of_moves
          """
        return self._number_of_moves

    def get_step(self):
        """
          Returns steps
          """
        return self._step


class player:
    """
    This class holds information about a player board, and whether they have a ring
    """

    def __init__(self):
        """
        Creates a player object
        """
        self._board = 0
        self._id = 0
        self._piece_color = ""

    def set_piece_color(self, piece):
        self._piece_color = piece

    def get_piece_color(self):
        return self._piece_color

    def set_board(self, board):
        """
        Sets a board input should be a base 2 int
        """
        self._board = board

    def get_board(self):
        """
        Gets the current board
        """
        return self._board

    def set_id(self, id):
        """
        Sets the id of the player
        """
        self._id = id

    def printboard(self):
        """
        Prints a fancy board for the player
        """
        piece = self._piece_color
        board = self._board
        counter = 1
        z = converttobinary(board)
        print("a     b    c    d    e    f    g    h    i    j    k    l    m    n    o    p    q    r    s    t")

        for element in z:
            if element == "1":
                print(piece, " ", end="")
            if element == "0":
                print("blk", " ", end="")

            if counter % 20 == 0:
                print(':', end="")
                print(21 - int((counter / 20)))
                print('\n')
            if counter == 400:
                print(
                    "a     b    c    d    e    f    g    h    i    j    k    l    m    n    o    p    q    r    s    t")
                print('\n')
                print('\n')
                print('\n')
            counter = counter + 1

    def check_ring(self, table):
        """
        Checks for the existence of a ring
        """
        i = 1
        while i < 380:
            # No need to check every possible point we can search an entire line at once
            # By skipping lines this seems to be faster in some causes
            line = converttobinary(table)[i:i + 19].find("101")
            if line == -1:
                i = i + 20
                continue

            # Now we implement the old code
            else:
                i = i + line

                for j in range(line, 15, 1):

                    if converttobinary(table)[i:i + 3] != "101":
                        i = i + 1
                        continue
                    if converttobinary(table)[i + 20:i + 23] != "111":
                        i = i + 1
                        continue
                    if converttobinary(table)[i - 20:i - 17] == "111":
                        return True
                i = i + 5

    def print_rings_only(self):
        """
        This function prints rings only. In Raw Text.
        """
        table = self.get_board()
        emptytable = converttobinary(0)
        full = ""
        i = 0
        while i < 400:
            t = bin(table)[2:].zfill(400)[i:i + 3]
            t2 = bin(table)[2:].zfill(400)[i + 20:i + 23]
            t3 = bin(table)[2:].zfill(400)[i + 40:i + 43]
            if bin(table).zfill(400)[i:i + 3] == "111" and bin(table).zfill(400)[i + 20:i + 23] == "101" and bin(
                    table).zfill(400)[i + 40:i + 43] == "111":
                full = full + converttobinary(table)[i:i + 3] + emptytable[i + 3:i + 20] + converttobinary(table)[
                                                                                           i + 20:i + 23] + emptytable[
                                                                                                            i + 23:i + 40] + converttobinary(
                    table)[i + 40:i + 43]
                i = i + 43
            else:
                full = full + emptytable[i]
                i = i + 1

        counter = 1
        for element in full:
            print(element, end="")
            if counter % 20 == 0:
                print('\n')
            counter = counter + 1

class GessGame:
    """
    This class holds information about all the players. The Current Games status, and who's turn it is.
    Functions are used to move pieces for individual players, and switch players if moves are valid. If a game is won or resign this function
    will return False for a move, and will return the winner for status check

    """

    def __init__(self):
        """
        Creates a game with players with all required variables set
        """
        self._player1 = player()
        self._player1.set_board(
            int("000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "000000000000000000000000000000000000000000000000000000001001001001001001000000000000000000000"
                "000000000000000000000001010111111110101000111010111101010111000101011111111010100000000000000"
                "00000000", 2))
        self._player2 = player()
        self._player2.set_board(
            int("0000000000000000000000101011111111010100011101011110101011100010101111111101010000000000000000"
                "0000000000000000000000000000100100100100100100000000000000000000000000000000000000000000000000"
                "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "000000000000000000000000", 2))

        self._player1.set_id(1)
        self._player2.set_id(2)
        self._player1.set_piece_color("\033[48;5;18mpl1\033[0m")
        self._player2.set_piece_color("\033[48;5;229mpl2\033[0m")
        self._currentplayer = self._player1
        self._otherplayer = self._player2
        self._edge = int(
            "1111111111111111111110000000000000000001100000000000000000011000000000000000000110000000000000000"
            "0011000000000000000000110000000000000000001100000000000000000011000000000000000000110000000000000"
            "0000011000000000000000000110000000000000000001100000000000000000011000000000000000000110000000000"
            "0000000011000000000000000000110000000000000000001100000000000000000011000000000000000000111111111"
            "111111111111", 2)
        self._game_state = "UNFINISHED"

    def get_player(self, player):
        """
        Returns a player object
        """
        if player == 1:
            return self._player1
        if player == 2:
            return self._player2
        else:
            return "Come on It's 1 or 2"

    def get_currentplayer(self):
        """
        Prints info about the current players
        """
        if self._currentplayer == self._player1:
            return "Current:Player 1 \nOther:Player 2"
        if self._currentplayer == self._player2:
            return "Current:Player 2\nOther:Player 1"

    def set_game_state(self, state):
        """
        Sets if the games is finished or if a player has won:
        """
        self._game_state = state

    def switch_player(self):
        """
        Changes who the currentplayer is
        """
        if self._currentplayer == self._player1:
            self._currentplayer = self._player2
            self._otherplayer = self._player1
        elif self._currentplayer == self._player2:
            self._currentplayer = self._player1
            self._otherplayer = self._player2

    def boardmovement(self, piece, step):
        """
         This function moves pieces on a board. Using bitwise operations
        """
        if step < 0:
            piece = piece >> (step * -1)
        else:
            piece = piece << step
        return piece

    def lookup(self, pos):
        """
        Checks to make sure that the position is within the board, and outputs a number based on that positions
        place on the board with  a20=399
        """
        posletter = pos[0]
        # convert upper to lower if needed
        if posletter.isupper():
            posletter = posletter.lower()
        posletter = ord(posletter)

        if posletter > 115 or posletter < 98:
            return False
        posnumber = int(pos[1:])

        if posnumber > 19 or posnumber < 2:
            return False
        location = (20 * posnumber - 1) - (posletter - 97)
        return location

    def printboard(self):
        """
        Prints a fancy board for the whole game
        """
        templist = []
        board1 = self.get_player(1).get_board()
        board2 = self.get_player(2).get_board()
        board1 = converttobinary(board1)
        board2 = converttobinary(board2)

        for i in range(400):
            templist.append("\033[38;5;7mblk \033[0m" + " ")

        for i, value in enumerate(board1):
            if value == "1":
                templist[i] = self.get_player(1).get_piece_color() + " "

        for i, value in enumerate(board2):
            if value == "1":
                templist[i] = self.get_player(2).get_piece_color() + " "
        print("a     b    c    d    e    f    g    h    i    j    k    l    m    n    o    p    q    r    s    t")

        counter = 1
        for element in templist:
            print(element, end="")

            if counter % 20 == 0:
                print(':', end="")
                print(21 - int((counter / 20)))
                print('\n')
            if counter == 400:
                print(
                    "a     b    c    d    e    f    g    h    i    j    k    l    m    n    o    p    q    r    s    t")
                print('\n')
                print('\n')
                print('\n')
            counter = counter + 1

    def make_move(self, midst, midend):
        """
        moves pieces on a tempboards if all checks pass it sets the corresponding tempboards
        as a board for the player objects. Otherwise nothing changes for either player
        """

        if self._game_state != 'UNFINISHED':
            return False
        startlocation = self.lookup(midst)
        endlocation = self.lookup(midend)
        if startlocation == False or endlocation == False:
            return False
        ne = 0
        n = 0
        nw = 0
        sw = 0
        se = 0
        s = 0
        e = 0
        w = 0

        # middle is also postion 5
        middle = startlocation
        if self._currentplayer == self._player1:
            currentplayer = self._player1
            otherplayer = self._player2
        elif self._currentplayer == self._player2:
            currentplayer = self._player2
            otherplayer = self._player1
        table1 = currentplayer.get_board()
        table2 = otherplayer.get_board()

        # int values with a scale of 2 when combined with tables it corresponds to specific location with each step to left increase by *2
        pos4 = quickpow(middle + 1)
        pos5 = quickpow(middle)
        pos6 = quickpow(middle - 1)
        pos1 = quickpow(middle + 21)
        pos2 = quickpow(middle + 20)
        pos3 = quickpow(middle + 19)
        pos7 = quickpow(middle - 19)
        pos8 = quickpow(middle - 20)
        pos9 = quickpow(middle - 21)

        # Move piece because if any section of piece hits another piece on the board we have to stop
        movepiece = pos1 | pos2 | pos3 | pos4 | pos5 | pos6 | pos7 | pos8 | pos9

        # actual piece
        piece = movepiece & table1

        # check if we have the other players stone
        if movepiece & table2 != 0:
            return False

        # exclusive or so piece isn't checked against itself.
        tablefull = (table1 ^ piece) | table2
        table1 = (table1 ^ piece)
        if self._currentplayer.check_ring(table1) == False:
            return False

        # change if need be
        if pos1 & piece != 0:
            nw = 3
        if pos2 & piece != 0:
            n = 3
        if pos3 & piece != 0:
            ne = 3
        if pos4 & piece != 0:
            w = 3

        if pos6 & piece != 0:
            e = 3

        if pos7 & piece != 0:
            se = 3
        if pos8 & piece != 0:
            s = 3
        if pos9 & piece != 0:
            se = 3

        # change max move to infinite if piece is in middle and direction is not zero
        maxlist = [nw, n, ne, w, e, sw, s, se]
        if pos5 & piece != 0:
            i = 0
            while i < 8:
                maxlist[i] = maxlist[i] * 99999
                i = i + 1

        # define movements, check if moves within max
        checkmove = movement()
        if checkmove.movenentor(startlocation, endlocation, maxlist) == False:
            return False
        else:
            nbmoves = checkmove.get_number_of_moves()
            step = checkmove.get_step()

        # check if move stops on a stone or moves are depleted

        for i in range(nbmoves):
            # need to move both at the same time
            piece = self.boardmovement(piece, step)
            movepiece = self.boardmovement(movepiece, step)

            # each step_movement we do these checks
            if piece & self._edge != 0:
                removepiece = piece & self._edge
                piece = piece ^ removepiece

            if tablefull & movepiece != 0 and i == nbmoves - 1:
                table1 = table1 ^ (table1 & movepiece)
                table1 = table1 | piece
                table2 = table2 ^ (table2 & movepiece)
                break

            elif tablefull & movepiece == 0 and i == nbmoves - 1:
                table1 = table1 ^ (table1 & movepiece)
                table1 = table1 | piece
                table2 = table2 ^ (table2 & movepiece)
                break

            elif tablefull & movepiece != 0 and i < nbmoves - 1:
                return False

        # Should only be done if destination has deplemeted all moves. In that case whether their is a ring or not
        # is a valid concern
        if self._currentplayer.check_ring(table1) == False:
            return False
        if self._otherplayer.check_ring(table2) == False:
            print(self._currentplayer)
            self.set_winner()
            return False
        # switch set succesful tables and switchplayers
        self._currentplayer.set_board(table1)
        self._otherplayer.set_board(table2)
        self.switch_player()
        return True

    """
    Return the status of the game
    """

    def get_game_state(self):
        return self._game_state

    """
    Will assign winner to the non-current player. Note: this does not take anything as a parameter
    """

    def resign_game(self):
        if self._currentplayer == self._player1:
            self.set_game_state('WHITE_WON')
        else:
            self.set_game_state('BLACK_WON')

    """
      Will assign winner to the current player. Note: this does not take anything as a parameter.
      This is called within the make_move function
    """

    def set_winner(self):
        if self._currentplayer == self._player1:
            self.set_game_state('BLACK_WON')
        else:
            self.set_game_state('WHITE_WON')
