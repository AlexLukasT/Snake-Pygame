# simple snake-based game using pygame

import pygame
import numpy as np
import time


def main():
    game = Game(200, 200, 2)
    game.run()


class Game():

    def __init__(self, screen_width, screen_height, scale=1):

        pygame.init()

        if screen_width % 10 == 0 and screen_height % 10 == 0:
            self.screen_width = screen_width * scale
            self.screen_height = screen_height * scale
        else:
            raise SetupError("Screen width and screen height have to be multiple of 10!")

        self.scale = scale

        self.colors = {"white": (255, 255, 255), "black": (0, 0, 0), "dark_green": (0, 102, 0), "red": (230, 0, 0)}

        self.length = 10 * scale

        self.head_pos_x = int(self.screen_width/(3*self.length)) * self.length 
        self.head_pos_y = int(self.screen_height/(2*self.length)) * self.length

        self.food_pos_x = np.random.randint(int(self.screen_width / self.length)) * self.length
        self.food_pos_y = np.random.randint(int(self.screen_height / self.length)) * self.length

        self.snake_list = []  # contains the fields which represent the snake
        self.snake_length = 1

        self.velocity = 10 * scale  # snake moves automatically by x px/loop
        self.direction = 1  # direction of the snake, default is right

        self.score = 0

        self.fontsize = 20 * self.scale

        self.startGame = False  # true if the player clicks "play" or "play again"
        self.gameExit = False  # true if the player hits a wall or the snake
        self.won = False
        self.pause = False

        self.gameDisplay = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake")

    def player_controls(self):
        # lets the player change the direction and exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = 0  # left
                if event.key == pygame.K_RIGHT:
                    self.direction = 1  # right
                if event.key == pygame.K_UP:
                    self.direction = 2  # up
                if event.key == pygame.K_DOWN:
                    self.direction = 3  # down
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause

    def draw_snake(self, color):
        # the head is constantly moving by 10 px and every position is added to self.snake_list
        # as long as self.snake_list is longer than the length of the snake, the last positions will be removed
        self.snake_list.append((self.head_pos_x, self.head_pos_y))
        while len(self.snake_list) > self.snake_length:
            del self.snake_list[0]
        for x, y in self.snake_list:
            pygame.draw.rect(self.gameDisplay, self.colors[color], [x, y, self.length, self.length])

    def move(self):
        # changes the direction by adding the velocity to different directions
        if self.direction == 0:  # left
            self.head_pos_x -= self.velocity
        elif self.direction == 1:  # right
            self.head_pos_x += self.velocity
        elif self.direction == 2:  # up
            self.head_pos_y -= self.velocity
        elif self.direction == 3:  # down
            self.head_pos_y += self.velocity

    def check_corner_collision(self):
        # checks if the head of the snake leaves the screen
        horizontal_collision = self.head_pos_x < 0 or self.head_pos_x > self.screen_width - self.length
        vertical_collision = self.head_pos_y < 0 or self.head_pos_y > self.screen_height - self.length
        if horizontal_collision or vertical_collision:
            self.gameExit = True

    def check_snake_collision(self):
        # checks if the head of the snake enters a field already entered by the tail
        for x, y in self.snake_list[:-1]:  # without the head
            if self.head_pos_x == x and self.head_pos_y == y:
                self.gameExit = True

    def print_score(self):
        # prints the current score on the screen
        font = pygame.font.SysFont(None, 10 * self.scale)
        score = font.render("Score: {}".format(self.score), True, self.colors["black"])
        self.gameDisplay.blit(score, [0, 0])

    def set_food(self):
        # sets a random generated piece of food on the screen and generates a new one if the current one gets
        # eaten
        pygame.draw.rect(self.gameDisplay, self.colors["red"],
                         [self.food_pos_x, self.food_pos_y, self.length, self.length])
        if self.head_pos_x == self.food_pos_x and self.head_pos_y == self.food_pos_y:
            # due to the snake head having a length and with of 10 px and the velocity of 10 px per loop the
            # display is discretised in fields of 10 x 10 px, so checking for overlapping in the left top
            # corner is enough
            self.food_pos_x = np.random.randint(int(self.screen_width / self.length)) * self.length
            self.food_pos_y = np.random.randint(int(self.screen_width / self.length)) * self.length
            self.score += 1
            self.snake_length += 1

    def create_text(self, title, posy):
        # creates text on the screen

        font = pygame.font.SysFont(None, self.fontsize)
        text = font.render(title, True, self.colors["black"])
        size = font.size(title)
        posx = (self.screen_width - size[0]) / 2
        self.gameDisplay.blit(text, [posx, posy])

    def create_button(self, title, posx, posy, width, height, color, action=None):
        # creates a button with the functionality to start or quit the game

        pygame.draw.rect(self.gameDisplay, color, [posx, posy, width, height])
        font = pygame.font.SysFont(None, self.fontsize)
        text = font.render(title, True, self.colors["black"])
        textw, texth = font.size(title)
        textx = posx + width / 2 - textw / 2
        texty = posy + height / 2 - texth / 2
        self.gameDisplay.blit(text, [textx, texty])

        mousex, mousey = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if posx < mousex < posx + width and posy < mousey < posy + height:
            if click[0] == 1 and action is not None:
                if action == "play":
                    self.reset()
                    self.gameExit = False
                    self.startGame = True
                elif action == "quit":
                    pygame.quit()
                    quit()

    def reset(self):
        # resets all the values to start a new game

        self.length = 10 * self.scale
        self.head_pos_x = int(self.screen_width/(3*self.length)) * self.length 
        self.head_pos_y = int(self.screen_height/(2*self.length)) * self.length
        self.snake_list = []
        self.snake_length = 1
        self.direction = 1
        self.score = 0

    def start_screen(self):
        # manages the screen when starting the game

        self.player_controls()

        width = 50 * self.scale
        height = 25 * self.scale

        self.gameDisplay.fill(self.colors["white"])

        self.create_text("Welcome to Snake!", 10 * self.scale)

        buttonx = self.screen_width / 2 - width / 2
        button1y = self.screen_height / 4 - height / 2
        self.create_button("Play", buttonx, button1y, width, height, self.colors["dark_green"], "play")

        button2y = self.screen_height / 2 - height / 2
        self.create_button("Quit", buttonx, button2y, width, height, self.colors["red"], "quit")

        self.create_text("Press space to pause", 3 * self.screen_height / 4)

    def aftergame_screen(self, mode):
        # manages the screen after a game was finished without winning

        self.player_controls()

        self.gameDisplay.fill(self.colors["white"])

        if mode == "lost":
            self.create_text("Game Over!", 10 * self.scale)
        elif mode == "won":
            self.create_text("Congratulations, you won!")

        self.create_text("You reached a score of {}".format(self.score), self.screen_height / 4, )

        width1 = 100 * self.scale
        height = 25 * self.scale

        button1x = self.screen_width / 2 - width1 / 2
        button1y = self.screen_height / 2 - height / 2
        self.create_button("Play again", button1x, button1y, width1, height, self.colors["dark_green"], "play")

        width2 = 50 * self.scale
        button2x = self.screen_width / 2 - width2 / 2
        button2y = 3 * self.screen_height / 4 - height / 2
        self.create_button("Quit", button2x, button2y, width2, height, self.colors["red"], "quit")

    def game_loop(self):
        # main loop, updates the screen

        if self.score == (self.screen_width / self.length) * (self.screen_height / self.length):  # max score
            self.won = True

        self.player_controls()

        self.gameDisplay.fill(self.colors["white"])
        pygame.draw.line(self.gameDisplay, self.colors["black"], (0, 0), (self.screen_width, 0), 1)

        self.print_score()
        self.set_food()
        self.move()
        self.draw_snake("dark_green")
        self.check_corner_collision()
        self.check_snake_collision()

        time.sleep(0.1)

    def run(self):
        # runs the game, manages start screen, pausing, finishing and game loop

        while True:
            if not self.startGame:  # enter start screen, clicking "play" sets startGame = True
                self.start_screen()
            elif self.gameExit:  # player crashes, enter loosing screen
                self.aftergame_screen("lost")
            elif self.won:  # player won
                self.aftergame_screen("won")
            elif self.pause:  # player presses space, game pauses
                self.player_controls()  # still need controls while game is paused to unpause or leave the game
                continue
            else:  # run the game
                self.game_loop()
            pygame.display.update()


class SetupError(Exception):

    def __init__(self, message):
        self.message = message


if __name__ == "__main__":
    main()
