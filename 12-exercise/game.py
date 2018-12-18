

class Game():

    def __init__(self, name):
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
        self.next = 1
        self.name = name
        self.status = None
        self.full = False

    def status(self):
        return self.status

    def play(self, player, x, y):

        if self.next == player:

            if x < 0 or x > 2 or y < 0 or y > 2:
                return 'bad', 'x:{}, y:{} is outside board range'.format(x, y)
            elif self.board[x][y] == 0:
                self.board[x][y] = player
                self.next = 1 if player == 2 else 2
                if self._check_victory(x, y):
                    self.status = player
                elif self._check_draw():
                    self.status = 0
                return 'ok', 'ok'
            else:
                return 'bad', '{}, {} is already occupied'.format(x, y)

        else:
            return 'bad', 'It is player\'s {} turn'.format(self.next)

    def _check_victory(self, x, y):
        #check if previous move caused a win on vertical line
        if self.board[0][y] == self.board[1][y] == self.board[2][y]:
            return True

        #check if previous move caused a win on horizontal line
        if self.board[x][0] == self.board[x][1] == self.board[x][2]:
            return True

        #check if previous move was on the main diagonal and caused a win
        if x == y and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True

        #check if previous move was on the secondary diagonal and caused a win
        if x + y == 2 and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True

        return False

    def _check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True
