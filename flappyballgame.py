import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screenwidth = 720
screenheight = 720
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption("Flappy Ball")

# Font for score
font = pygame.font.Font(None, 36)

# Create the ball object
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

        # Prevent the ball from going below the screen
        if self.y + self.radius > screenheight:
            self.y = screenheight - self.radius
            self.velocity = 0

        # Prevent the ball from going above the screen
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def draw(self):
        pygame.draw.circle(screen, (255, 204, 0), (int(self.x), int(self.y)), self.radius)


# Create the pipes
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
        # Draw the top pipe
        pygame.draw.rect(screen, (34, 139, 34), (int(self.x), 0, self.width, self.top_pipe))
        # Draw the bottom pipe
        pygame.draw.rect(screen, (34, 139, 34), (int(self.x), screenheight - self.bottom_pipe, self.width, self.bottom_pipe))

    def off_screen(self):
        return self.x + self.width < 0


# Create the game
class Game:
    def __init__(self):
        self.ball = Ball()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.ball = Ball()
        self.pipes = []
        self.score = 0
        self.game_over = False

    def check_collision(self):
        for pipe in self.pipes:
            # Check horizontal overlap
            if self.ball.x + self.ball.radius > pipe.x and self.ball.x - self.ball.radius < pipe.x + pipe.width:
                # Check vertical collision
                if self.ball.y - self.ball.radius < pipe.top_pipe or self.ball.y + self.ball.radius > screenheight - pipe.bottom_pipe:
                    return True
        return False

    def play_step(self):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.ball.jump()
                if self.game_over and event.key == pygame.K_r:
                    self.reset()

        # Clear the screen
        screen.fill((135, 206, 235))  # Light blue background

        # Move the ball
        self.ball.move()
        self.ball.draw()

        # Check for collision
        if self.check_collision():
            self.game_over = True
            return -10, self.game_over, self.score  # Negative reward for collision

        # Add new pipes
        if len(self.pipes) == 0 or self.pipes[-1].x < screenwidth // 2:
            self.pipes.append(Pipes())

        # Move and draw pipes
        for pipe in self.pipes:
            pipe.move()
            pipe.draw()
            # Check if the ball has passed a pipe (for scoring)
            if pipe.x + pipe.width < self.ball.x and not hasattr(pipe, 'scored'):
                self.score += 1
                pipe.scored = True  # Mark the pipe as scored

        # Remove off-screen pipes
        self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

        # Display the score
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))  # Display at top-left corner

        # Update the display
        pygame.display.update()
        self.clock.tick(60)

        return 10, self.game_over, self.score  # Positive reward for staying alive


# Main game loop
if __name__ == "__main__":
    game = Game()
    while True:
        reward, game_over, score = game.play_step()
        if game_over:
            print(f"Game Over! Final Score: {score}")
            print("Press 'R' to restart") 

