import numpy as np

class Mastermind():

    def __init__(self, size=4, min_value=1, max_value=9, rand=True):

        self.size = size
        self.min_val = min_value
        self.max_val = max_value
        if rand:
            self.board = np.random.randint(low=self.min_val, high=self.max_val, size=self.size)
            

    def set_board(self, board):
        self.board = board
        self.size = len(board)

    def check(self, guess):
        
        correct = np.all(guess == self.board)
        result = [0] * self.size

        #Display the correct squares
        for i, element in enumerate(guess):
            if element == self.board[i]:
                result[i] = 2
            elif element in self.board:
                result[i] = 1
            else:
                result[i] = 0
        
        return result


    def play(self):

        print("Welcome to Mastermind 1.0!")
        turn = 0
        guess = np.zeros((self.size))
        while not(np.all(guess == self.board)):

            turn += 1
            print(f"This is your {turn} guessing turn!")
            guess = list(map(int,input("Enter the numbers : ").strip().split()))[:self.size] 
            print(guess)
            guess = np.array(guess)

            result = [0] * self.size

            #Display the correct squares
            for i, element in enumerate(guess):

                if element == self.board[i]:
                    result[i] = 2
                elif element in self.board:
                    result[i] = 1
                else:
                    result[i] = 0

            print("The result of your guess: ", result)

        print("Yes, you have guessed it correctly!")
        return -1


if __name__ == "__main__":
    game = Mastermind(size=4, min_value=1, max_value=3)
    game.play()