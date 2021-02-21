from mastermind import Mastermind
import numpy as np

class MastermindAI():

    def __init__(self):
        self.board = Mastermind(size=4, min_value=1, max_value=3)
        self.board_size = self.board.size
        self.min = 1
        self.max = 9

        self.known = {}
        self.existed = set()
        self.cannot = {
            i: set()
            for i in range(self.board_size)
        }
        self.not_existed = set()

    def set_board(self, board):
        self.board = board
        self.board_size = board.size

    def make_guess(self):
        """
        Make a guess based on current knowledge
        """
        guess = [0] * self.board_size
        for i in range(self.board_size):

            possible_values = []

            #If a position is known to be correct:
            if i in self.known:
                guess[i] = self.known[i]

            #If not, check for other conditions
            else:
                for value in range(self.min, self.max + 1):
                    if value in self.cannot[i] or value in self.not_existed:
                        pass
                    else:
                        possible_values.append(value)
            
                #Make a random choice from the possible values
                guess[i] = np.random.choice(possible_values)

        return guess

    def solve(self):
        turn = 0
        guesses = []
        print("The board: ", self.board.board)
        done = False
        while not done:

            guess = self.make_guess()
            guesses.append(guess)
            print(f"The AI guesses: {guess}")

            #Check for results
            results = self.board.check(guess)
            print(f"The results the AI gets: {results}")
            if np.all(results == ([2] * self.board_size)):
                done = True
                pass

            #Append new knowledge
            for i, result in enumerate(results):

                if result == 2:
                    self.known[i] = guess[i]
                    self.existed.add(guess[i])
                elif result == 1:
                    self.existed.add(guess[i])
                    self.cannot[i].add(guess[i])
                else:
                    self.not_existed.add(guess[i])

        return guesses

            
if __name__ == "__main__":
    board = Mastermind(size=4, min_value=1, max_value=4)
    AI = MastermindAI(board)
    AI.solve()