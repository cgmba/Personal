'''
Four in a row

Author: Tony Lindgren
Student: Godwin Mba
'''
from copy import deepcopy
#from time import process_time, process_time_ns

class FourInARow:
    def __init__(self, player, chip):
        new_board = []
        for _ in range(7):
            new_board.append([])
        self.board = new_board
        self.action = list(range(7))
        if chip != 'r' and chip != 'w':
            print('The provided value is not a valid chip (must be, r or w): ', chip)
        if player == 'human' and chip == 'w':
            self.ai_player = 'r'
        else:
            self.ai_player = 'w'
        self.curr_move = chip
    
    def to_move(self):
        return self.curr_move
        
    #actions
    ########TODO
    def actions(self):
        action_list = []
        for i in range(len(self.board)):
            if len(self.board[i]) < 6:
                action_list.append(i)
        return action_list


    ########
    def column_multiplier(self, cm, count):
        
        if cm == 3:
            return count*4
        elif cm == 2 or cm == 4:
            return count * 3
        elif cm == 1 or cm == 5:
            return count*2
        elif cm == 0 or cm == 6:
            return count

    #######

    #eval
    #TODO
    def eval(self, state, curr_move):
        
        ai_latest_move = None
        if curr_move == 'r':
            ai_latest_move = 'w'
        else:
            ai_latest_move = 'r'
        score = 0
        for i in range(len(self.board)):
            score += self.column_multiplier(i, state.board[i].count(ai_latest_move))
        return score



    def result(self, action):                    
        dc = deepcopy(self)
        if self.to_move() == 'w':
            dc.curr_move = 'r'
            dc.board[action].append(self.to_move())   
        else:
            dc.curr_move = 'w'
            dc.board[action].append(self.to_move())            
        return dc
        
    
        
    def is_terminal(self):
        #check vertical
        for c in range(0, len(self.board)):
            count = 0
            curr_chip = None
            for r in range(0, len(self.board[c])):
                if curr_chip == self.board[c][r]:
                    count = count + 1
                else:
                    curr_chip = self.board[c][r]     
                    count = 1
                if count == 4:
                    if self.ai_player == curr_chip:        
                        #print('Found vertical win')
                        return True, 100          #MAX ai wins positive utility
                    else:
                        #print('Found vertical loss')
                        return True, -100         #MIN player wins negative utility
                    
        #check horizontal 
        #TODO   
        ############
        k = 0 
        for i in range(len(max(self.board, key=len))): 
            count = 0
            curr_chip = None
            for j in range(len(self.board)):
                try: 
                    if curr_chip == self.board[j][k]:
                        count += 1
                    else:
                        curr_chip = self.board[j][k]     
                        count = 1
                    if count == 4:
                        if self.ai_player == curr_chip:
                            # print('Found horizontal win')
                            return True, 100
                        else:
                            return True, -100
                except IndexError: 
                    
                    count = 0
            k += 1 
        

        #check positive diagonal
        for c in range(7-3): 
            for r in range(6-3):    
                if len(self.board[c]) > r and len(self.board[c+1]) > r+1 and len(self.board[c+2]) > r+2 and len(self.board[c+3]) > r+3:
                    if self.ai_player == self.board[c][r] and self.ai_player == self.board[c+1][r+1] and self.ai_player == self.board[c+2][r+2] and self.ai_player == self.board[c+3][r+3]:  
                        #print('Found positive diagonal win')
                        return True, 100
                    elif self.ai_player != self.board[c][r] and self.ai_player != self.board[c+1][r+1] and self.ai_player != self.board[c+2][r+2] and self.ai_player != self.board[c+3][r+3]:  
                        #print('Found positive diagonal loss')
                        return True, -100
        
        #check negative diagonal 
        #TODO   
        # d = 5
        # ################
        # for c in range(7 - 3):
        #     for r in range(6 - 3):
        #         if len(self.board[d]) > r and len(self.board[d - 1]) > r > 1 and len(self.board[d - 2]) > r + 2 and len(
        #                 self.board[d - 3]) > r + 3:
        #             if self.ai_player == self.board[d][r] and self.ai_player == self.board[d - 1][
        #                 r + 1] and self.ai_player == self.board[d - 2][r + 2] and self.ai_player == self.board[d - 3][
        #                 r + 3]:
        #                 #print('Found negative diagonal win')
        #                 return True, 100
        #             elif self.ai_player != self.board[d][r] and self.ai_player != self.board[d - 1][
        #                 r + 1] and self.ai_player != self.board[d - 2][r + 2] and self.ai_player != self.board[d - 3][
        #                 r + 3]:
        #                 #print('Found negative diagonal loss')
        #                 return True, -100
        #     d-=1


        ######

        b = 5
        for c in range(7-4): 
            for r in range(6-3):    
                if len(self.board[b]) > r and len(self.board[b-1]) > r+1 and len(self.board[b-2]) > r+2 and len(self.board[b-3]) > r+3:
                    if self.ai_player == self.board[b][r] and self.ai_player == self.board[b-1][r+1] and self.ai_player == self.board[b-2][r+2] and self.ai_player == self.board[b-3][r+3]:  
                        # print('Found negative diagonal win')
                        return True, 100
                    elif self.ai_player != self.board[b][r] and self.ai_player != self.board[b-1][r+1] and self.ai_player != self.board[b-2][r+2] and self.ai_player != self.board[b-3][r+3]:  
                        return True, -100
            b -= 1
        #check draw
        #TODO  

        ######
        ###
        
        
        if all(len(i) == 6 for i in self.board):
             return True, 0

        return False, 0
                                                  
                
    #########pretty_print

    # def pretty_print(board):
    #     rows = ['a','b','c','d','e','f']
    #     top = '    1   2   3   4   5   6   7   '
    #     row = [[n] for n in range(0,7)]
    #     row[0][0] = 'f | '
    #     row[1][0] = 'e | '
    #     row[2][0] = 'd | '
    #     row[3][0] = 'c | '
    #     row[4][0] = 'b | '
    #     row[5][0] = 'a | '
    #     print('')
    #     print('  ' + '-'*(len(top)-3))
    #     for j in range(0,len(rows)):
    #         for i in range(1,8):
    #             row[j][0] = row[j][0] + str(board[j][i-1]) + ' | '
    #         print(row[j][0])
    #         print('  ' + '-'*((len(row[j][0])-3)))
    #     print(top)
    #     print('')
    # #  ##TODO

    #######



    def pretty_print(self):
        
        dc = deepcopy(self.board)

        for c in range(len(dc)):
            if len(dc[c]) != 6:
                for _ in range(6 - len(dc[c])):
                    dc[c].append("_")

        for i in range(7):
            print(i, "", end="")
        print()
        for r in range(5, -1, -1):
            for c in range(7):
                print(dc[c][r], end=" ")
            print()

        