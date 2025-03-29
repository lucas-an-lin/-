import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Run")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

gravity = 1.0
jump_power = -15

dino_y = HEIGHT - 60
velocity_y = 0
score = 0
last_obstacle = None
last_spawn_time = 0

class Dinosaur:
    def __init__(self):
        self.image = pygame.Rect(50, HEIGHT - 60, 40, 40)
        self.velocity_y = 0
        self.is_jumping = False
        self.is_ducking = False
    
    def jump(self):
        if not self.is_jumping:
            self.velocity_y = jump_power
            self.is_jumping = True

    def duck(self):
        self.is_ducking = True
        self.image.height = 20

    def stand(self):
        self.is_ducking = False
        self.image.height = 40

    def update(self):
        self.velocity_y += gravity
        self.image.y += self.velocity_y
        if self.image.y >= HEIGHT - 60:
            self.image.y = HEIGHT - 60
            self.velocity_y = 0
            self.is_jumping = False

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def move(self):
        self.rect.x -= 5
    
    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)

clock = pygame.time.Clock()
dino = Dinosaur()
obstacles = []
running = True

def spawn_obstacle():
    global last_obstacle, last_spawn_time
    current_time = time.time()
    if current_time - last_spawn_time >= random.uniform(0.5, 2):
        if random.randint(0, 100) < 5:
            if last_obstacle == "cactus":
                new_obstacle = Obstacle(WIDTH, HEIGHT - 90, 30, 20)
                last_obstacle = "bird"
            else:
                new_obstacle = Obstacle(WIDTH, HEIGHT - 60, 20, 40)
                last_obstacle = "cactus"
            obstacles.append(new_obstacle)
            last_spawn_time = current_time

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dino.jump()
            elif event.key == pygame.K_DOWN:
                dino.duck()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                dino.stand()
    
    dino.update()
    pygame.draw.rect(screen, BLACK, dino.image)
    
    spawn_obstacle()
    for obstacle in obstacles[:]:
        obstacle.move()
        obstacle.draw()
        if obstacle.rect.x < -20:
            obstacles.remove(obstacle)
    
    for obstacle in obstacles:
        if dino.image.colliderect(obstacle.rect):
            font = pygame.font.Font(None, 50)
            game_over_text = font.render("Game Over", True, BLACK)
            options_text = font.render("R-restart  Q-leave", True, BLACK)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 30))
            screen.blit(options_text, (WIDTH//2 - options_text.get_width()//2, HEIGHT//2 + 20))
            pygame.display.flip()
            
            game_over = True
            while game_over:
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        obstacles.clear()
                        dino = Dinosaur()
                        score = 0
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False
                        game_over = False
                elif event.type == pygame.QUIT:
                    running = False
                    game_over = False
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()