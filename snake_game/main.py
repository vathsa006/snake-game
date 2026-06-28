import pygame
import random
import os
import sys

# Initialize pygame and mixer (for audio)
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    # Fail silently if no audio device is connected
    pass

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 12

# Colors (Modern Neon Palette)
COLOR_BG = (15, 12, 32)         # Deep midnight blue
COLOR_GRID = (25, 20, 52)       # Subtle grid lines
COLOR_SNAKE_HEAD = (0, 255, 180) # Neon teal
COLOR_SNAKE_BODY = (0, 180, 216) # Neon blue
COLOR_FOOD = (255, 0, 127)      # Neon pink/red
COLOR_TEXT = (240, 240, 255)
COLOR_MUTED = (120, 120, 160)
COLOR_PANEL = (25, 22, 50)

# Setup Game Window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("NEON SNAKE - Classic Game")
clock = pygame.time.Clock()

# High Score utility
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip())
        except ValueError:
            return 0
    return 0

def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except Exception:
        pass

# Particle effect system
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        self.lifetime = random.randint(10, 20)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            # Fade out
            alpha = int((self.lifetime / 20) * 255)
            r, g, b = self.color
            color_with_alpha = (r, g, b) # Pygame draw does not support alpha directly without a separate surface
            pygame.draw.circle(surface, color_with_alpha, (int(self.x), int(self.y)), 3)

class SnakeGame:
    def __init__(self):
        self.high_score = load_high_score()
        self.reset_game()

    def reset_game(self):
        # Start in the middle of the screen
        self.snake = [
            (GRID_WIDTH // 2, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
            (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)
        ]
        self.direction = (1, 0) # Moving right
        self.next_direction = (1, 0)
        self.score = 0
        self.spawn_food()
        self.particles = []
        self.game_over = False
        self.paused = False

    def spawn_food(self):
        while True:
            self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(1, GRID_HEIGHT - 1))
            # Make sure food doesn't spawn inside the snake
            if self.food not in self.snake:
                break

    def trigger_particle_burst(self, pos):
        # Trigger 15 particles when food is eaten
        px, py = pos[0] * GRID_SIZE + GRID_SIZE // 2, pos[1] * GRID_SIZE + GRID_SIZE // 2
        for _ in range(15):
            self.particles.append(Particle(px, py, COLOR_FOOD))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if self.game_over:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.reset_game()
                else:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif not self.paused:
                        if event.key in (pygame.K_UP, pygame.K_w) and self.direction != (0, 1):
                            self.next_direction = (0, -1)
                        elif event.key in (pygame.K_DOWN, pygame.K_s) and self.direction != (0, -1):
                            self.next_direction = (0, 1)
                        elif event.key in (pygame.K_LEFT, pygame.K_a) and self.direction != (1, 0):
                            self.next_direction = (-1, 0)
                        elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.direction != (-1, 0):
                            self.next_direction = (1, 0)

    def update(self):
        if self.game_over or self.paused:
            return

        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Boundary collisions
        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 1 or new_head[1] >= GRID_HEIGHT:
            self.trigger_game_over()
            return

        # Self collisions
        if new_head in self.snake:
            self.trigger_game_over()
            return

        # Insert new head
        self.snake.insert(0, new_head)

        # Eating food check
        if new_head == self.food:
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
                save_high_score(self.high_score)
            self.trigger_particle_burst(self.food)
            self.spawn_food()
        else:
            # Remove tail if didn't eat
            self.snake.pop()

        # Update particles
        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0:
                self.particles.remove(p)

    def trigger_game_over(self):
        self.game_over = True

    def draw_grid(self, surface):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, COLOR_GRID, (x, GRID_SIZE), (x, WINDOW_HEIGHT))
        for y in range(GRID_SIZE, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, COLOR_GRID, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        screen.fill(COLOR_BG)
        self.draw_grid(screen)

        # Draw Score bar panel at the top
        pygame.draw.rect(screen, COLOR_PANEL, (0, 0, WINDOW_WIDTH, GRID_SIZE * 1.5))
        font = pygame.font.SysFont("Outfit", 20, bold=True)
        score_text = font.render(f"SCORE: {self.score}", True, COLOR_TEXT)
        high_score_text = font.render(f"HIGH SCORE: {self.high_score}", True, COLOR_SNAKE_HEAD)
        screen.blit(score_text, (20, 5))
        screen.blit(high_score_text, (WINDOW_WIDTH - 200, 5))

        # Draw food (Neon pulse glow effect)
        fx, fy = self.food
        food_rect = pygame.Rect(fx * GRID_SIZE + 2, fy * GRID_SIZE + 2, GRID_SIZE - 4, GRID_SIZE - 4)
        pygame.draw.rect(screen, COLOR_FOOD, food_rect, border_radius=6)

        # Draw Snake
        for idx, segment in enumerate(self.snake):
            sx, sy = segment
            rect = pygame.Rect(sx * GRID_SIZE + 1, sy * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2)
            color = COLOR_SNAKE_HEAD if idx == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(screen, color, rect, border_radius=4)

        # Draw particles
        for p in self.particles:
            p.draw(screen)

        # Draw overlay screens (Pause / Game Over)
        if self.paused:
            self.draw_overlay("PAUSED", "Press 'P' to Resume")
        elif self.game_over:
            self.draw_overlay("GAME OVER", f"Your Score: {self.score} | Press 'Space' to Restart")

        pygame.display.flip()

    def draw_overlay(self, title, subtitle):
        # Semi-transparent overlay surface
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 8, 25, 200)) # Dark transparent background
        screen.blit(overlay, (0, 0))

        font_title = pygame.font.SysFont("Cinzel", 64, bold=True)
        font_sub = pygame.font.SysFont("Outfit", 24)

        title_render = font_title.render(title, True, COLOR_FOOD if "OVER" in title else COLOR_SNAKE_HEAD)
        sub_render = font_sub.render(subtitle, True, COLOR_TEXT)

        title_rect = title_render.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        sub_rect = sub_render.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))

        screen.blit(title_render, title_rect)
        screen.blit(sub_render, sub_rect)

def main():
    game = SnakeGame()
    
    # Start screen / main menu loop
    menu_active = True
    while menu_active:
        screen.fill(COLOR_BG)
        font_title = pygame.font.SysFont("Cinzel", 72, bold=True)
        font_sub = pygame.font.SysFont("Outfit", 22)
        
        # Neon glowing title effect
        title_val = font_title.render("NEON SNAKE", True, COLOR_SNAKE_HEAD)
        title_rect = title_val.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        screen.blit(title_val, title_rect)
        
        inst_text = [
            "Use WASD or ARROW keys to navigate",
            "Avoid wall boundaries and self-collision",
            "Press P to pause the game",
            "Press ENTER or SPACE to start the journey"
        ]
        
        y_offset = WINDOW_HEIGHT // 2
        for text in inst_text:
            text_val = font_sub.render(text, True, COLOR_MUTED if "Avoid" in text else COLOR_TEXT)
            text_rect = text_val.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            screen.blit(text_val, text_rect)
            y_offset += 35
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    menu_active = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(15)

    # Main Game Loop
    while True:
        game.handle_input()
        game.update()
        game.draw()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
