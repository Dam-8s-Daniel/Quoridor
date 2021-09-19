#Author: Daniel Dam
#Date: 7/28/21
#Description: This file creates the game of Quoridor. Quoridor is a two player game in which the goal is for a player
#to move their pawn from their baseline to the other player's baseline.



class Square:
    """
    Represents a square in a game of Quoridor with an (x,y) coordinate and a list of coordinates
    that represent the other squares that a pawn has access to.
    """
    def __init__(self, coordinate, ortho_move_list):
        """
        Initiates a square in a game of Quoridor. Each square has a coordinate (x,y) and a list of possible moves. It
        also can determine if a pawn is on it.
        :p1: coordinate -- represents a square's place on the board
        :p2: ortho_move_list -- list of possible moves. Updated as fences are placed.
        """
        self._square_coordinate = coordinate
        self._ortho_moves_list = ortho_move_list
        self._hfences = []
        self._vfences = []
        self._pawn = None

    def remove_pawn(self):
        """Removes a pawn."""
        self._pawn = None

    def get_pawn(self):
        """Determines if a pawn is on a Square. Returns Boolean."""
        return self._pawn

    def set_pawn(self, player):
        """Records which pawn is on the square."""
        self._pawn = player

    def get_square_coordinate(self):
        """Returns the coordinate (x,y) of the square"""
        return self._square_coordinate

    def get_ortho_moves(self):
        """Returns a list of possible moves for that square."""
        return self._ortho_moves_list

    def remove_ortho_moves(self, coordinate):
        """
        Removes a coordinate from the list of possible moves. This method is used when a fence is blocking a position.
        """
        self._ortho_moves_list.remove(coordinate)

    def set_fences(self, v_or_h, coordinate):
        """
        Adds a fence around a square.
        Updates the list of possible moves of the fence coordinate removing the coordinate that is being blocked.
        Updates the list of possible moves of the coordinate that is being blocked. (When a fence is placed, two
        squares are blocked from one another, so both squares must be updated).
        """
        if v_or_h == "h":
            self._hfences.append(coordinate)
            self.remove_ortho_moves(coordinate)
        if v_or_h == "v":
            self._vfences.append(coordinate)
            self.remove_ortho_moves(coordinate)


class QuoridorGame:
    """
    Class that creates a game of Quoridor. Takes no parameters.
    """

    def __init__(self):
        """Initializes board with pawns placed in their correct positions."""



        self._squares_list = [] #all the squares on the "board"
        self._board = self._squares_list
        self.create_squares() #creates all the squares on the board
        self.place_pawns_in_start_position() #places pawns in their correct starting position
        self._p1_position = (4,0)
        self._p2_position = (4,8)
        self._turn = 1
        self._game_won = False
        self._p1_fence_inventory = 10
        self._p2_fence_inventory = 10
        self._vFences = []
        self._hFences = []
        self._p1_baseline = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
        self._p2_baseline = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
        self._first_row = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
        self._first_column = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]

    def get_vFences(self):
        return self._vFences

    def get_hFences(self):
        return self._hFences

    def get_game_won(self):
        return self._game_won

    def get_player_turn(self):
        return self._turn

    def create_squares(self):
        """
        Creates instances of Squares with coordinates between (0,0) and (8,8).
        The Square objects are saved in list attribute in the QuoridorGame class.
        Takes no parameters.
        Returns: Square objects
        """
        for y in range(9):
            for x in range(9):
                coordinate = (x, y)
                ortho_move_list = [
                    (x, y - 1),  # top mid
                    (x - 1, y),  # mid left
                    (x + 1, y),  # mid right
                    (x, y + 1),  # bot mid
                ]
                #get rid of possible moves that are not on the board
                corrected_ortho_move_list = [coordinate for coordinate in ortho_move_list if -1 < coordinate[0] < 9 and -1 < coordinate[1] < 9]
                self._squares_list.append(Square(coordinate, corrected_ortho_move_list))

    def get_squares(self):
        """Returns the list of squares."""
        return self._squares_list

    def place_pawns_in_start_position(self):
        """Places pawns in the correct starting position at the beginning of the game."""
        p1_start_position = (4,0)
        p2_start_position = (4,8)
        self.find_square(p1_start_position).set_pawn(1)
        self.find_square(p2_start_position).set_pawn(2)

    def basic_checks(self, player, position):
        """
        Returns False if the game is won, the wrong player is moving, or the input position is not on the board.
        p1: integer representing player that is moving (1 or 2)
        p2: position -- tuple representing the coordinate that the player wants to move-to
        """
        # Can't move if the game is done.
        if self._game_won is True:
            return False
        # Can't move if the wrong player is moving
        elif self._turn != player:
            return False
        #cant move if position is none
        elif position[0] == None or position[1] == None:
            return False
        # postion must be on board
        elif position[0] < 0 or position[0] > 8 or position[1] < 0 or position[1] > 8:
            return False

    def get_position(self, player):
        """
        Returns position of a player.
        p1: player (1 or 2)
        returns: tuple representing player 1 or player 2 position
        """
        if player == 1:
            return self._p1_position
        else:
            return self._p2_position

    def get_other_player_position(self, player):
        """
        Given a player as a parameter, the function returns the opponent's position.
        """
        if player == 1:
            return self._p2_position
        else:
            return self._p1_position

    def set_pawn_position(self, player, new_position):
        """
        Places pawn in correct position and updates current and former positions.
        p1: player (1 or 2)
        p2: position that pawn is moving to
        """
        current_position = self.get_position(player)
        old_square = self.find_square(current_position)
        old_square.remove_pawn()
        new_square = self.find_square(new_position)
        new_square.set_pawn(player)
        if player == 1:
            self._p1_position = new_position
        else:
            self._p2_position = new_position

    def find_square(self, coordinate):
        """
        Returns the Square object of a given coordinate parameter.
        p1: tuple representing a coordinate on the board (x,y)
        """
        for square in self._squares_list:
            if coordinate == square.get_square_coordinate():
                return square

    def is_winner(self, player):
        """
        Returns boolean if input player is a winner.
        p1: player (1 or 2)
        """
        if player < 1 or player > 2:
            return "Please enter a correct player"
        if player == 1:
            if self._p1_position in self._p2_baseline:
                self._game_won = True
                return True
        if player == 2:
            if self._p2_position in self._p1_baseline:
                self._game_won = True
                return True
        return False

    def set_fence_inventory(self, player):
        """
        Decreases the amount of fences available to a player. Method is used after other methods that have placed a
        fence on the board.
        p1: player (1 or 2)
        """
        if player == 1:
            self._p1_fence_inventory -= 1
        else:
            self._p2_fence_inventory -= 1

    def fence_inventory(self, player):
        """
        Returns a boolean whether a player has a fence available to use.
        p1: player (1 or 2)
        """
        if player == 1:
            if self._p1_fence_inventory > 0:
                return True
            else:
                return False
        elif player == 2:
            if self._p2_fence_inventory > 0:
                return True
            else:
                return False

    def get_fence_inventory(self, player):
        """
        Returns inventory of a player's fence
        p1: player (1 or 2)
        """
        if player == 1:
            return self._p1_fence_inventory
        else:
            return self._p2_fence_inventory

    def set_player_turn(self, player):
        """
        Switches whose turn it is. If player 1 is entered, then player 2 is set next to player and vice versa.
        p1: player (1 or 2)
        """
        if player == 1:
            self._turn = 2
        else:
            self._turn = 1

    def is_vadjacent(self, player):
        """
        Returns an updated list of possible moves if two pawns are vertically adjacent to one another.
        Preconditions scenario 1: Jump is blocked
        Postconditions scenario 1: Return combination of the two's pawn's possible moves
        Preconditions scenario 2: Jump is not blocked
        Postconditions scenario 2: Return the pawn's current possible moves along with the jump-to coordinate
        p1: player that is moving (1 or 2)
        """
        current_coordinates = self.get_position(player)
        current_square = self.find_square(current_coordinates)
        current_basic_moves = current_square.get_ortho_moves()
        other_player_position = self.get_other_player_position(player)
        other_player_square = self.find_square(other_player_position)
        other_player_possible_moves = other_player_square.get_ortho_moves()
        x_difference = current_coordinates[0] - other_player_position[0]
        y_difference = current_coordinates[1] - other_player_position[1]

        if x_difference == 0 and y_difference == 1:
            #If jump is blocked, then return the combination of the two pawn's possible moves
            if (current_coordinates[0], current_coordinates[1] - 2) not in other_player_possible_moves:
                updated_moves = current_basic_moves + other_player_possible_moves
                return updated_moves
            else:
                #If jump is not blocked, then return the current pawn's moves with the jump move.
                updated_moves = current_basic_moves + [(current_coordinates[0], current_coordinates[1] - 2)]
                return updated_moves

        if x_difference == 0 and y_difference == -1:
            if (current_coordinates[0], current_coordinates[1] + 2) not in other_player_possible_moves:
                updated_moves = [current_basic_moves] + other_player_possible_moves
                return updated_moves
            else:
                updated_moves = current_basic_moves + [(current_coordinates[0], current_coordinates[1] + 2)]
                return updated_moves
        return current_basic_moves


    def is_hadjacent(self, player):
        """
        Returns an updated list of possible moves if two pawns are horizontally adjacent to one another.
        Preconditions scenario 1: Jump is blocked
        Postconditions scenario 1: Return combination of the two's pawn's possible moves
        Preconditions scenario 2: Jump is not blocked
        Postconditions scenario 2: Return the pawn's current possible moves along with the jump-to coordinate
        p1: player that is moving (1 or 2)
        """
        current_coordinates = self.get_position(player)
        current_square = self.find_square(current_coordinates)
        current_basic_moves = current_square.get_ortho_moves()
        other_player_position = self.get_other_player_position(player)
        other_player_square = self.find_square(other_player_position)
        other_player_possible_moves = other_player_square.get_ortho_moves()

        x_difference = current_coordinates[0] - other_player_position[0]
        y_difference = current_coordinates[1] - other_player_position[1]
        if x_difference == 1 and y_difference == 0:
            if (current_coordinates[0] - 2, current_coordinates[1]) not in other_player_possible_moves:
                updated_moves = current_basic_moves + other_player_possible_moves
                return updated_moves
            else:
                updated_moves = current_basic_moves + [(current_coordinates[0] - 2, current_coordinates[1])]
                return updated_moves

        if x_difference == -1 and y_difference == 0:
            if (current_coordinates[0] + 2, current_coordinates[1]) not in other_player_possible_moves:
                updated_moves = [current_basic_moves] + other_player_possible_moves
                return updated_moves
            else:
                updated_moves = current_basic_moves + [(current_coordinates[0] + 2, current_coordinates[1])]
                return updated_moves

        return current_basic_moves

    def basic_possible_moves(self, player, move_to_position):
        """
        Returns boolean whether desired move is possible.
        Methods used: is_vadjacent, is_hadajacent, find_square, get_ortho_moves, get_position
        p1: coordinates of desired move-to position
        """
        current_coordinates = self.get_position(player)
        current_square = self.find_square(current_coordinates)
        current_basic_moves = current_square.get_ortho_moves()
        other_player_position = self.get_other_player_position(player)
        other_player_square = self.find_square(other_player_position)
        other_player_possible_moves = other_player_square.get_ortho_moves()
        is_vadjacent = self.is_vadjacent(player)
        is_hadjacent = self.is_hadjacent(player)

        #Can't move pawn to it's current space or the other pawn's space.
        if move_to_position == self._p1_position or move_to_position == self._p2_position:
            return False

        #If new position is in the list of current basic moves for the square that the pawn is currently on, return True
        if move_to_position in current_basic_moves:
            return True
        elif move_to_position in is_vadjacent or move_to_position in is_hadjacent:
            return True
        else:
            return False


    def move_pawn(self, player, move_to_position):
        """Method that moves a pawn to a valid position. Uses basic_possible_moves to determine if move is legal.
        If true, pawn is set in new position using set_pawn_position method, then the player's turn is switched to the
        other player using set_player_turn method.
        p1: player that is moving
        p2: pawn destination (tuple coordinate, (x,y))
        """

        if self.basic_checks(player, move_to_position) is False:
            return False

        #Check to see if basic move to position is valid. If it is, set the pawn to new position and switch turns.
        if self.basic_possible_moves(player, move_to_position) is True:
            self.set_pawn_position(player, move_to_position)
            self.set_player_turn(player)
            self.is_winner(player)
            return True
        else:
            return False


    def fence_checks(self, player, position, vertical_or_horizontal):
        """
        Returns False if placement of the fence is incorrect. Uses basic_checks method to determine if input parameters
        are correct.
        p1: player (input as number 1 or 2)
        p2: coordinate of the position where the fence wants to be placed (tuple, (x,y))
        p3: "v" or "h" (for a vertically placed fence or horizontally placed fence)
        """
        if self.basic_checks(player, position) is False:
            return False

        #position can't be in the first column if "v" and position can't be in first row if "h"
        if (position in self._first_column and vertical_or_horizontal == "v") or (position in self._first_row and vertical_or_horizontal == "h"):
            return False

        #Inventory must be greater than 0 to place a fence
        if self.fence_inventory(player) is False:
            return False
        #Cant place fence where there is already one
        if (vertical_or_horizontal == "v" and position in self._vFences) or (vertical_or_horizontal == "h" and position in self._hFences):
            return False


    def place_fence(self, player, vertical_or_horizontal, position):
        """
        Method that places a fence after using other methods to determine if fence placement is correct.
        The fence is placed on the top right corner of the square and extends down for "v" or to the right for "h".
        p1: 1 or 2 for the player.
        p2: "v" or "h" for vertical or horizontal placement
        p3: tuple (x,y) coordinate of where the fence wants to be placed
        """

        #check valid parameters
        if self.fence_checks(player, position, vertical_or_horizontal) is False:
            return False

        #find the square of corresponding coordinates
        square = self.find_square(position)

        #If fence placement is possible, update the list of fences and possible position in those blocked positions
        if vertical_or_horizontal == "v":
            self._vFences += [position]
            square.set_fences("v", (position[0]-1, position[1]))
            adjacent = self.find_square((position[0] - 1, position[1]))
            adjacent.set_fences("v", position)
            self.set_fence_inventory(player)
            self.set_player_turn(player)
            return True

        elif vertical_or_horizontal == "h":
            self._hFences += [position]
            square.set_fences("h", (position[0], position[1]-1))
            adjacent = self.find_square((position[0], position[1]-1))
            adjacent.set_fences("h", position)
            self.set_fence_inventory(player)
            self.set_player_turn(player)
            return True
        else:
            return False






