
import random
from ship import Ship
from board import Board
from position import Position


# This is a naive implementation of a Player class that:
# 1. Sets up the same board every time (i.e. a static layout)
# 2. Fires randomly, without remembering which shots were hits and misses
class Player:

    # Each player has a name. There should be no need to change or delete this!
    def __init__(self, name):
        self.__name = name
        self.__results = []
        self.rc_list = []
        self.final = []
        self.__next_move_rc = []
        self.target = False #flag to indicate if there is a hit
        self.target_rc = [] #maintains a list of immediate rc hits

    def get_name(self):
        return self.__name

    def __str__(self):
        return self.get_name()

    # get_board should return a Board object containing 5 ships:
    # 1 aircraft carrier (length = 5)
    # 1 battleship (length = 4)
    # 1 cruiser (length = 3)
    # 1 submarine (length = 3)
    # 1 destroyer (length = 2)
    # You can make your own fun names for the ships, but the number and lengths
    # of the ship will be validated by the framework. Printing the board will
    # show the first letter of each ship's name.

    # This implementation returns the first sample layout from this web page:
    # http://datagenetics.com/blog/december32011/index.html
    def get_board(self):

        #randomly selects one of the three ship positions
        a = [Ship('Carrier', Position('C', 2), 5, True),
             Ship('battleship', Position('C', 8), 4, True),
             Ship('submarine', Position('A', 2), 3, False),
             Ship('crusier', Position('D', 9), 3, True),
             Ship('destroyer', Position('H', 2), 2, False)]

#        ships_list[0] = [Ship('Carrier', Position('C', 2), 5, True),
#             Ship('battleship', Position('F', 7), 4, True),
#             Ship('submarine', Position('A', 2), 3, False),
#             Ship('crusier', Position('D', 9), 3, True),
#             Ship('destroyer', Position('A', 5), 2, True)]
#
#        ships_list[1] = [Ship('Carrier', Position('C', 2), 5, True),
#             Ship('battleship', Position('F', 5), 4, True),
#             Ship('submarine', Position('A', 2), 3, False),
#             Ship('crusier', Position('D', 9), 3, True),
#             Ship('destroyer', Position('B', 7), 2, True)]

        b = [Ship('Carrier', Position('D', 2), 5, True),
             Ship('battleship', Position('F', 5), 4, True),
             Ship('submarine', Position('I', 8), 3, False),
             Ship('crusier', Position('D', 9), 3, True),
             Ship('destroyer', Position('B', 7), 2, True)]

        c = [Ship('Carrier', Position('E', 6), 5, True),
             Ship('battleship', Position('F', 3), 4, True),
             Ship('submarine', Position('B', 1), 3, True),
             Ship('crusier', Position('D', 9), 3, True),
             Ship('destroyer', Position('B', 7), 2, True)]

        i = random.randint(0,2)
#
#        return Board(ships_list[i])
        if i == 0:
            return Board(a)
        elif i == 1:
            return Board(b)
        elif i == 2:
            return Board(c)
#        return Board(a)

    def diagonal_list(self):
        n = 0
        dia_list = []

        while n < 5:
            i1 = 0
            j1 = 2*n
            i2 = 2*n
            j2 = 0
            for i in range(1,11-2*n):
                if n == 0:
                    dia_list.append([chr(64 + i1 + i), j1 +i])
                else:
                    dia_list.append([chr(64 + i1 + i), j1 +i])
                    dia_list.append([chr(64 + i2 + i), j2 +i])
            n += 1
        return dia_list

    # Takes a random shot, making no effort to remember it
    def next_shot(self):
        if len(self.rc_list) == 0:
            self.final = self.diagonal_list()
        if len(self.final) != 0:
            [row, col], self.final = self.final[-1], self.final[:-1]
        else:
            row = chr(64 + random.randint(1, 10))  # A - J
            col = random.randint(1, 10)
        forward = False

        if self.__next_move_rc != []:
            [row, col] = self.__next_move_rc.pop()
        else:
            while forward == False:
                if [row, col] in self.rc_list:
                    row = chr(64 + random.randint(1, 10))  # A - J
                    col = random.randint(1, 10)
                else:
                    forward = True

        return Position(row, col)

    #function to find missing elements in a sequence.
    #this is used to get next potential target position
    def find_missing(self, lst):
        start = lst[0]
        end = lst[-1]
        return sorted(set(range(start, end + 1)).difference(lst))

    # result is a tuple consisting of:
    # - the shot location (a Position object)
    # - whether the shot was a hit (True) or a miss (False)
    # - whether a ship was sunk (True) or not (False)
    def post_shot_result(self, result):
        self.__results.append(result)
        self.rc_list.append([chr(result[0].get_row_idx() + 65), result[0].get_col_idx() + 1])

        #check if ship is sunk
        if result[1] == True and result[2] == True:
            self.target = False
            self.__next_move_rc = []
            self.target_rc = []

        #check if it is a miss when the target is true
        #this is useful in cases when our first hit is somewhere in the middle of a ship
        if result[1] == False and result[2] == False and self.target == True:
#            self.counter +=1
#            if self.counter >2:
#                self.target = False
#                self.__next_move_rc = []
#                self.target_rc = []
#
            if len(self.target_rc) == 1:
                #we do nothing because we want to check the remaining possible positions
                    a = 0

            else:
            #redo things using preceeding block
                self.__next_move_rc = []
                row1 = self.target_rc[0][0]
                col1 = self.target_rc[0][1]
                self.target_rc.append([row1,col1])

                if row1 == self.target_rc[1][0]:
                    #it means that the ship is horizontal
                    #focus on row as next move
                    #this time, reverse
                    #left
                    row = row1
                    col = self.target_rc[0][1] -1
                    p = Position(row, col)
                    #we add the position to the next move if two conditions are met
                    #1. If it is a valid position
                    #2. It has not been bombed already
                    if p.validate() and [row, col] not in self.rc_list:
                        self.__next_move_rc.append([row, col])

                elif col1 == self.target_rc[1][1]:
                    #it means that the ship is vertical
                    #focus on column as next move

                    #top
                    row = chr(ord(self.target_rc[0][0])-1)
                    col = col1
                    p = Position(row, col)
                    #we add the position to the next move if two conditions are met
                    #1. If it is a valid position
                    #2. It has not been bombed already
                    if p.validate() and [row, col] not in self.rc_list:
                        self.__next_move_rc.append([row, col])

        #check if ship is hit
        if result[1] == True and result[2] == False:
            #Check if this was a first hit
            if self.target == False:
                #first hit confirmed!
                #set target flag and update target row-column in target list
                self.target=True
                self.target_rc.append([chr(result[0].get_row_idx() + 65), result[0].get_col_idx() + 1])

                #list out possible next positions one by one
                #left
                row = chr(result[0].get_row_idx() + 65)
                col = result[0].get_col_idx() + 0
                p = Position(row, col)
                if p.validate():
                    self.__next_move_rc.append([row, col])

                #top
                row = chr(result[0].get_row_idx() + 64)
                col = result[0].get_col_idx() + 1
                p = Position(row, col)
                if p.validate():
                    self.__next_move_rc.append([row, col])

                #right
                row = chr(result[0].get_row_idx() + 65)
                col = result[0].get_col_idx() + 2
                p = Position(row, col)
                if p.validate():
                    self.__next_move_rc.append([row, col])

                #bottom
                row = chr(result[0].get_row_idx() + 66)
                col = result[0].get_col_idx() + 1
                p = Position(row, col)
                if p.validate():
                    self.__next_move_rc.append([row, col])

            elif self.target_rc != [] and self.target == True:
                #we conclude that the current hit is a continuation of previous hit
                #we now target positions based on whether ship is in same row or same column
                self.__next_move_rc = []
                row1 = chr(result[0].get_row_idx() + 65)
                col1 = result[0].get_col_idx() + 1
                self.target_rc.append([row1,col1])

                if row1 == self.target_rc[0][0]:
                    #it means that the ship is horizontal
                    #focus on row as next move
                    #left
                    row = row1
                    col = result[0].get_col_idx() + 0
                    p = Position(row, col)
                    #we append the position to the next move if two conditions are met
                    #1. If it is a valid position
                    #2. It has not been bombed already
                    if p.validate() and [row, col] not in self.rc_list:
                        self.__next_move_rc.append([row, col])
                    #right
                    row = row1
                    col = result[0].get_col_idx() + 2
                    p = Position(row, col)
                    #we append the position to the next move if two conditions are met
                    #1. If it is a valid position
                    #2. It has not been bombed already
                    if p.validate() and [row, col] not in self.rc_list:
                        self.__next_move_rc.append([row, col])

                elif col1 == self.target_rc[0][1]:
                    #it means that the ship is vertical
                    #focus on column as next move

                    #top
                    row = chr(result[0].get_row_idx() + 64)
                    col = col1
                    p = Position(row, col)
                    #we append the position to the next move if two conditions are met
                    #1. If it is a valid position
                    #2. It has not been bombed already
                    if p.validate() and [row, col] not in self.rc_list:
                        self.__next_move_rc.append([row, col])

                    #bottom
                    row = chr(result[0].get_row_idx() + 66)
                    col = col1
                    p = Position(row, col)
                    #we append the position to the next move if two conditions are met
                    #1. If it is a valid position
                    #2. It has not been bombed already
                    if p.validate() and [row, col] not in self.rc_list:
                        self.__next_move_rc.append([row, col])
