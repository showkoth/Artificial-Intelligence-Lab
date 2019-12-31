import random

class minimax:

    def __init__(self):
        self.board = []
        for i in range(9):
            self.board.append(" ")
    
    def clearBoard(self):
        for i in range(9):
            self.board[i] = " "
        

    def showBoard(self):
        for i in range(9):
            print(self.board[i] + " |", end = " ")
            if (i+1) % 3 == 0:
                print()

    def checkWinner(self):
        winPositions = ([0, 1, 2], [3, 4, 5], [6, 7, 8],
                  [0, 3, 6], [1, 4, 7], [2, 5, 8],
                  [0, 4, 8], [2, 4, 6])
        players = ("X", "O")
        for player in players:
            playerPositions = self.getDoneMoves(player)  # returns a list of position
            for posi in winPositions:
                win = True
                for pos in posi:
                    if pos not in playerPositions:
                        win = False
                if win:
                    return player

    def isGameOver(self):
        if self.checkWinner() != None:
            return True
        for pos in self.board:
            if pos == " ":
                return False
        return True
    

    def Winner(self):
        if self.checkWinner() == "X":
            return "X"
        elif self.checkWinner() == "O":
            return "Computer"
        elif self.isGameOver() == True:
            return "Match Drawn"

    def updateBoard(self, position, player):
        self.board[position] = player

    def getAvailableMoves(self):
        moves = []
        for i in range(9):
            if self.board[i] == " ":
                moves.append(i)
        return moves

    def getDoneMoves(self, player):
        moves = []
        for i in range(9):
            if self.board[i] == player:
                moves.append(i)
        return moves


    def Minmax(self, board, depth, player):
        
        if depth == 0 or board.isGameOver():
            if board.checkWinner() == "X":
                return 0
            elif board.checkWinner() == "O":
                return 100
            else:
                return 50

        if player == "O":
            bestValue = 0
            for move in board.getAvailableMoves():
                board.updateBoard(move, player)
                moveValue = self.Minmax(board, depth-1, FlipPlayer(player))
                board.updateBoard(move, " ")
                bestValue = max(bestValue, moveValue)
            return bestValue
        
        if player == "X":
            bestValue = 100
            for move in board.getAvailableMoves():
                board.updateBoard(move, player)
                moveValue = self.Minmax(board, depth-1, FlipPlayer(player))
                board.updateBoard(move, " ")
                bestValue = min(bestValue, moveValue)
            return bestValue

def FlipPlayer(player):
    if player == "X":
        return "O"
    else:
        return "X"

def make_best_move(board, depth, player):
    
    neutralValue = 50
    choices = []
    for move in board.getAvailableMoves():
        board.updateBoard(move, player)
        moveValue = board.Minmax(board, depth-1, FlipPlayer(player))
        board.updateBoard(move, " ")

        if moveValue > neutralValue:
            choices = [move]
            break
        elif moveValue == neutralValue:
            choices.append(move)

    if len(choices) > 0:
        return random.choice(choices)
    else:
        return random.choice(board.getAvailableMoves())




if __name__ == '__main__':
    game = minimax()
    game.showBoard()
    all_moves = []
    while not game.isGameOver():
        person_move = int(input("Choose number from 1 to 9: "))
        game.updateBoard(person_move-1, "X")
        game.showBoard()
        all_moves.append(person_move)

        if game.isGameOver():
            break

        print("Minimax is choosing move...")
        minmax_move = make_best_move(game, -1, "O")
        game.updateBoard(minmax_move, "O")
        game.showBoard()
        all_moves.append(minmax_move)

print("Game Over. " + game.Winner() + " Wins")
