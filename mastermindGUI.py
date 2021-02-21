import pygame
import numpy as np
from mastermind import Mastermind
from mastermindAI import MastermindAI

class MainGUI():

    def __init__(self):
        self.HEIGHT, self.WIDTH = 400, 600
        self.BLACK = (0, 0, 0)
        self.WHITE = (255 , 255 , 255)
        self.game = Mastermind()
        self.size = self.game.size

        #Initialize the window
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mastermind 1.0")
        self.screen.fill((self.BLACK))

    def launch(self):

        intro_menu = introMenu(self.screen, (self.BLACK, self.WHITE), (self.WIDTH, self.HEIGHT))
        event = intro_menu.launch()

        #When the button is clicked
        if event == 0:
            main_screen = mainGame(self.screen, (self.BLACK, self.WHITE), (self.WIDTH, self.HEIGHT), self.size, self.game)
            main_screen.launch()

        elif event == 1:
            AI = MastermindAI()
            main_screen_ai = mainGameAI(self.screen, (self.BLACK, self.WHITE), (self.WIDTH, self.HEIGHT), self.size, self.game, AI)
            main_screen_ai.launch()
        
        else:
            print("Pygame quitted")
            return -1

    
class introMenu():

    def __init__(self, screen, colors, size):
        self.screen = screen
        self.BLACK, self.WHITE = colors 
        self.WIDTH, self.HEIGHT = size
        self.text = "Welcome to Mastermind 1.0!"
        self.LARGE_FONT = pygame.font.Font("OpenSans-Regular.ttf", 30)
        self.SMALL_FONT = pygame.font.Font("OpenSans-Regular.ttf", 20)
        self.buttons = []

    def draw(self):

        #Draw the text
        intro_text = self.LARGE_FONT.render(self.text, True, self.WHITE)
        intro_text_rect = intro_text.get_rect()
        intro_text_rect.center = (self.WIDTH / 2, 100)
        self.screen.blit(intro_text, intro_text_rect)

        #Draw the human button
        button_human = self.LARGE_FONT.render("Click here to begin: Human guesses", True, self.BLACK)
        button_human_rect = button_human.get_rect()
        button_human_rect.center = (self.WIDTH / 2, 200)
        self.buttons.append(button_human_rect)
        pygame.draw.rect(self.screen, self.WHITE, button_human_rect)
        self.screen.blit(button_human, button_human_rect)

        #Draw the AI button
        button_AI = self.LARGE_FONT.render("Click here to begin: AI guesses", True, self.BLACK)
        button_AI_rect = button_AI.get_rect()
        button_AI_rect.center = (self.WIDTH / 2, 270)
        self.buttons.append(button_AI_rect)
        pygame.draw.rect(self.screen, self.WHITE, button_AI_rect)
        self.screen.blit(button_AI, button_AI_rect)

        #Update the view
        pygame.display.update()


    def launch(self):
        self.draw()

        #The waiting loop
        while True:
            for event in pygame.event.get():

                #Check for events in the main menu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return -1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, button in enumerate(self.buttons):
                        if button.collidepoint(pos):
                            return i



class mainGame():

    def __init__(self, screen, colors, gui_size, size, game):
        self.screen = screen
        self.BLACK, self.WHITE = colors 
        self.GREEN, self.RED, self.YELLOW = (0, 255, 0), (255, 0, 0), (255, 255, 0)
        self.WIDTH, self.HEIGHT = gui_size
        self.LARGE_FONT = pygame.font.Font("OpenSans-Regular.ttf", 30)
        self.MID_FONT = pygame.font.Font("OpenSans-Regular.ttf", 25)
        self.SMALL_FONT = pygame.font.Font("OpenSans-Regular.ttf", 20)
        self.buttons = []
        self.game = game
        self.board_size = size
        self.answer = [-1] * self.board_size

    def backend_play(self, guess):
        """
        Perform playing in the background
        """
        result = self.game.check(guess)
        return result

    def draw_text(self, text, color, center_pos, left_coor, font):

        #Draw the text
        text_to_draw = font.render(text, True, color)

        if center_pos:
            text_to_draw_rect = text_to_draw.get_rect()
            text_to_draw_rect.center = center_pos
            self.screen.blit(text_to_draw, text_to_draw_rect)

        elif left_coor:
            self.screen.blit(text_to_draw, left_coor)

        #Update the display
        pygame.display.update()


    def draw_outline(self, rect, color):
        pygame.draw.rect(self.screen, color, rect, 3)
        pygame.display.update()

    def draw_entered_guess(self, number, rect):

        if number: 
            self.draw_text(str(number), self.BLACK, rect.center, None, self.SMALL_FONT)
        else:
            pygame.draw.rect(self.screen, self.WHITE, rect)
            self.draw_outline(rect, self.GREEN)


    def draw_past_guess(self, guess, turn, hist_board):
        """
        Draw the past guesses from the user
        """
        topleft_x, topleft_y = hist_board.topleft
        text = f" {turn}. {guess}"
        self.draw_text(text, self.WHITE, None, (topleft_x + 10, topleft_y + 10 + (turn-1)*30), self.SMALL_FONT)
        pygame.display.update()


    def draw_result_squares(self, result=[0,0,0,0]):

        #Draw text
        self.draw_text("The results", self.WHITE, None, (50, 150), self.LARGE_FONT)

        #Draw the results
        for i in range(self.board_size):
            rect = pygame.Rect(50 + i*(35 + 15), 200, 35, 35)

            #Draw the result squares, depending on the result
            if result[i] == 0:
                color = self.RED
            elif result[i] == 1:
                color = self.YELLOW
            else:
                color = self.GREEN
            pygame.draw.rect(self.screen, color, rect)

        #Update display
        pygame.display.update()


    def draw_guessing_squares(self, text="Your guess"):

        #Delete other components on the screen
        self.screen.fill((self.BLACK))

        #Draw the text on the playing side
        self.draw_text(text, self.WHITE, None, (50, 30), self.LARGE_FONT)

        #Draw the board
        for i in range(self.board_size):
            rect = pygame.Rect(50 + i*(35 + 15), 100, 35, 35)
            self.buttons.append(rect)
            pygame.draw.rect(self.screen, self.WHITE, rect)

        #Update the display
        pygame.display.update()


    def draw_scoreboard(self, turn, text1="Your guesses: ", text2="Your past guess"):

        #Draw the turn
        self.screen.fill((self.BLACK), pygame.Rect((350, 30, 220, 40)))
        self.draw_text(text1 + f"{turn}", self.WHITE, None, (350, 30), self.MID_FONT)

        #Draw the history
        self.draw_text(text2, self.WHITE, None, (350, 80), self.MID_FONT)
        hist_board = pygame.Rect((350, 130, 200, 250))
        pygame.draw.rect(self.screen, self.WHITE, hist_board, 1)
        
        #Update the display
        pygame.display.update()     

        return hist_board


    def winning(self, text="You solved it!"):
        """
        Create a winning text
        """
        self.draw_text(text, self.RED, None, (50, 320), self.LARGE_FONT)


    def keyboard_pressed(self, event):
        """
        Return the value of the pressed keyboard
        """
        if event.key == pygame.K_0:
            return 0
        if event.key == pygame.K_1:
            return 1
        if event.key == pygame.K_2:
            return 2
        if event.key == pygame.K_3:
            return 3
        if event.key == pygame.K_4:
            return 4
        if event.key == pygame.K_5:
            return 5
        if event.key == pygame.K_6:
            return 6
        if event.key == pygame.K_7:
            return 7
        if event.key == pygame.K_8:
            return 8
        if event.key == pygame.K_9:
            return 9
        if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
            return "delete"
        if event.key == pygame.K_RETURN:
            return "submit"
        if event.key == pygame.K_LEFT:
            return "left"
        if event.key == pygame.K_RIGHT:
            return "right"


    def launch(self):
        self.draw_guessing_squares()
        self.draw_result_squares()
        hist_board = self.draw_scoreboard(0)
        previous = 0
        turn = 0

        while True:
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    #Handling the clicking of the squares
                    for i, square in enumerate(self.buttons):
                        if square.collidepoint(pos):
                            self.draw_outline(self.buttons[previous], self.BLACK)
                            self.draw_outline(square, self.GREEN)
                            previous = i

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

                #The user enters from a keyboard
                if event.type == pygame.KEYDOWN:
                    output = self.keyboard_pressed(event)

                    if isinstance(output, int):
                        self.draw_entered_guess(output, self.buttons[previous])

                        #Handling error 
                        #TODO
                        if output > 5:
                            #Do something
                            pass
                        #If the answer is not full, then raise an error

                        self.answer[previous] = output
                        
                    if output == "delete":
                        self.draw_entered_guess(None, self.buttons[previous])

                    if output == "submit":
                        turn += 1
                        result = self.backend_play(self.answer)
                        hist_board = self.draw_scoreboard(turn)
                        self.draw_result_squares(result)
                        self.draw_past_guess(self.answer, turn, hist_board)

                        #Check for winning
                        if np.all(result == ([2] * self.board_size)):
                            self.winning()

                    if output == "left":
                        self.draw_outline(self.buttons[previous], self.BLACK)
                        previous -= 1
                        if previous == -1:
                            previous = self.board_size - 1
                        self.draw_outline(self.buttons[previous], self.GREEN)

                    if output == "right":
                        self.draw_outline(self.buttons[previous], self.BLACK)
                        previous += 1
                        if previous == self.board_size:
                            previous = 0
                        self.draw_outline(self.buttons[previous], self.GREEN)


class mainGameAI(mainGame):
    def __init__(self, screen, colors, gui_size, size, game, AI):
        super().__init__(screen, colors, gui_size, size, game)
        self.AI = AI

    def launch(self):
        self.draw_guessing_squares(text="Your test")
        hist_board = self.draw_scoreboard(0, text1="AI guesses: ", text2="AI past guesses")
        previous = 0
        turn = 0

        while True:
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    #Handling the clicking of the squares
                    for i, square in enumerate(self.buttons):
                        if square.collidepoint(pos):
                            self.draw_outline(self.buttons[previous], self.BLACK)
                            self.draw_outline(square, self.GREEN)
                            previous = i

                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False

                #The user enters from a keyboard
                if event.type == pygame.KEYDOWN:
                    output = self.keyboard_pressed(event)

                    if isinstance(output, int):
                        self.draw_entered_guess(output, self.buttons[previous])

                        #Handling error 
                        #TODO
                        if output > 5:
                            #Do something
                            pass
                        #If the answer is not full, then raise an error

                        self.answer[previous] = output

                    if output == "left":
                        self.draw_outline(self.buttons[previous], self.BLACK)
                        previous -= 1
                        if previous == -1:
                            previous = self.board_size - 1
                        self.draw_outline(self.buttons[previous], self.GREEN)

                    if output == "right":
                        self.draw_outline(self.buttons[previous], self.BLACK)
                        previous += 1
                        if previous == self.board_size:
                            previous = 0
                        self.draw_outline(self.buttons[previous], self.GREEN)
                        
                    if output == "delete":
                        self.draw_entered_guess(None, self.buttons[previous])

                    if output == "submit":
                        min_val = min(self.answer)
                        max_val = max(self.answer)
                        size = len(self.answer)
                        board = Mastermind(size=size, min_value=min_val, max_value=max_val, rand=False)
                        board.set_board(self.answer)
                        self.AI.set_board(board)
                        guesses = self.AI.solve()
                        hist_board = self.draw_scoreboard(len(guesses), text1="AI guesses: ", text2="AI past guesses")
                        for i in range(len(guesses)):
                            self.draw_past_guess(guesses[i], i+1, hist_board)

                        self.winning(text="AI solves it!")


if __name__ == "__main__":
    GUI = MainGUI()
    GUI.launch()

        


