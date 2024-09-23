# Othello Board
# enmpy area = -1
# player: white=1, black=0
#
#   a b c d e f g h
# 1                
# 2                
# 3                
# 4                
# 5                
# 6                
# 7                
# 8                

import math

class OthelloAlgorithm:
    BOARD_WIDTH = 8
    BOARD_HEIGHT = 8
    BOARD_WIDTH_MID = int(BOARD_WIDTH/2)
    BOARD_HEIGHT_MID = int(BOARD_HEIGHT/2)

    NONE = -1

    def __init__(self):
        self.board = [[self.NONE for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        self.board[self.BOARD_HEIGHT_MID-1][self.BOARD_WIDTH_MID-1] = self.board[self.BOARD_HEIGHT_MID][self.BOARD_WIDTH_MID] = 1
        self.board[self.BOARD_HEIGHT_MID-1][self.BOARD_WIDTH_MID] = self.board[self.BOARD_HEIGHT_MID][self.BOARD_WIDTH_MID-1] = 0

        self.player = 0
        self.game_end = False

        self.can_reverse_list = [] # 各入力候補の裏返せるリスト

    def _check(self, x, y):
        if self.board[y][x] != self.NONE:
            return False

        can_reverse_list = []
        for i in range(8):
            a, b = x, y
            dx = round(math.cos(i*math.pi/4))
            dy = round(math.sin(i*math.pi/4))

            tmp_reverse_list = []
            while 0<=a+(dx*2)<self.BOARD_WIDTH and 0<=b-(dy*2)<self.BOARD_HEIGHT:
                a += dx
                b -= dy
                if self.board[b][a] == self.player or self.board[b][a] == self.NONE:
                    break

                tmp_reverse_list.append([a,b])
                if self.board[b-dy][a+dx] == self.player:
                    can_reverse_list.append(tmp_reverse_list)
                    break
        return _list if (_list := can_reverse_list) else False

    def get_square_list(self):
        all_can_put_list = []
        all_can_reverse_list = []
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                if self.board[y][x] == -1:
                    if check_result := self._check(x,y):
                        all_can_put_list.append([x,y])
                        all_can_reverse_list.append(check_result)
        return list(zip(all_can_put_list, all_can_reverse_list)) if all_can_put_list else False

    def _reverse_discs(self, reverse_list):
        for disc in reverse_list:
            for x, y in disc:
                self.board[y][x] = self.player

    def put_disc(self,x,y):
        if square_list := self.get_square_list():
            if reverse_list:=next((i[1] for i in square_list if i[0] == [x,y]), False):
                self.board[y][x] = self.player
                self._reverse_discs(reverse_list)
                self.player ^= 1
                return square_list
        return False

    def get_disc_count(self):
        white_disc_count = 0
        black_disc_count = 0
        for y in range(self.BOARD_HEIGHT):
            for x in range(self.BOARD_WIDTH):
                if self.board[y][x] == 0:
                    black_disc_count+=1
                if self.board[y][x] == 1:
                    white_disc_count+=1
        return black_disc_count, white_disc_count

    def cli_put_disc(self):
        self.cli_print_board()
        print("White" if self.player == 1 else "Black")

        xy = input("input: ")
        if not xy:
            return False
        # xy = [ i for i in xy if i!=' ' ]
        # x, y = xy
        x = xy[0]
        # y = [i for i in xy[1:] if i!=' ']
        y = xy[1:].replace(' ', '')
        #TODO############################
        # if type(y) is int:
        #     return False
        # print(x,y)

        if ord(x)%97 > self.BOARD_WIDTH-1 or int(y)-1 > self.BOARD_HEIGHT-1:
            print("?")
            return False

        x = ord(x)%97
        y = int(y)-1
        if not self.put_disc(x,y):
            print("Not put.")

    def cli_print_board(self):
        space_size = len(str(self.BOARD_HEIGHT))

        print(' '*space_size + ' ', end='')
        for x in range(97, 97+self.BOARD_WIDTH):  #96~123 a~z
            print(chr(x), end=' ')

        print()
        for y in range(self.BOARD_HEIGHT):
            print((' '*(space_size-len(str(y+1))) + str(y+1)) if y<(10**(space_size-1)-1) else y+1, end=' ')
            for x in range(self.BOARD_WIDTH):
                print('▯' if self.board[y][x] == self.NONE else self.board[y][x], end=' ')
            print()

if __name__ == '__main__':
    def game_play():
        othello = OthelloAlgorithm()
        while True:
            if not othello.get_square_list():
                othello.player ^= 1
                if not othello.get_square_list():
                    black_num, white_num = othello.get_disc_count()
                    if black_num > white_num:
                        print(black_num, "Winner Black!!")
                    elif black_num < white_num:
                        print(white_num, "Winner White!!")
                    elif black_num == white_num:
                        print("Draw.")
                    break
                else:
                    print("Black" if othello.player == 1 else "White", "pass")

            othello.cli_put_disc()
    game_play()
