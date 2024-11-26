import pygame
import random
import numpy as np

pygame.init()

screenwidth = 720
screenheight = 720
screen = pygame.display.set_mode((screenwidth, screenheight))


class Ball:
    def __init__(self):
        self.x = 100
        self.y = screenheight // 2
        self.radius = 40
        self.velocity = 0
        self.gravity = 0.5
        self.up = -10

    def jump(self):
        self.velocity = self.up

    def move(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y + self.radius > screenheight:
            self.y = screenheight - self.radius
            self.velocity = 0

        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def draw(self):
        pygame.draw.circle(screen, (255, 204, 0), (int(self.x), int(self.y)), self.radius)


class Pipes:
    def __init__(self):
        self.x = screenwidth
        self.width = 50
        self.gap = 200
        self.top_pipe = random.randint(50, screenheight - self.gap - 50)
        self.bottom_pipe = screenheight - self.top_pipe - self.gap
        self.velocity = 5

    def move(self):
        self.x -= self.velocity

    def draw(self):
        pygame.draw.rect(screen, (34, 139, 34), (int(self.x), 0, self.width, self.top_pipe))
        pygame.draw.rect(screen, (34, 139, 34),
                         (int(self.x), screenheight - self.bottom_pipe, self.width, self.bottom_pipe))

    def off_screen(self):
        return self.x + self.width < 0


class Game:
    def __init__(self):
        self.ball = Ball()
        self.pipes = []
        self.score = 0
        self.game_over = False

    def check_collision(self):
        for pipe in self.pipes:
            if (self.ball.x + self.ball.radius > pipe.x and self.ball.x - self.ball.radius < pipe.x + pipe.width):
                if self.ball.y - self.ball.radius < pipe.top_pipe:
                    return True
                if self.ball.y + self.ball.radius > screenheight - pipe.bottom_pipe:
                    return True
        return False

    def reset_game(self):
        self.ball = Ball()
        self.pipes = []
        self.score = 0
        self.game_over = False

    def game_state(self):
        if self.game_over is False:
            return np.array([self.ball.y, self.ball.velocity, self.pipes[0].top_pipe, self.pipes[0].bottom_pipe, self.score,])


    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            screen.fill((137, 232, 148))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        self.ball.jump()
                    if self.game_over and event.key == pygame.K_r:
                        self.reset_game()

            if not self.game_over:
                self.ball.move()
                self.ball.draw()

                if len(self.pipes) == 0 or self.pipes[-1].x < screenwidth // 2:
                    self.pipes.append(Pipes())

                for pipe in self.pipes[:]:
                    pipe.move()
                    pipe.draw()

                    if pipe.off_screen():
                        self.pipes.remove(pipe)
                        self.score += 1

                if self.check_collision():
                    self.game_over = True
                    print("you died... lol")
                    print(self.score)
            pygame.display.flip()
            print(self.game_state())

game = Game()
game.run()

