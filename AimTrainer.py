import pygame
import random
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Load sound
pop_sound = pygame.mixer.Sound('pop_sound.wav')  # Replace with the path to your sound file

# Screen settings
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Aim Trainer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
DARK_GREY = (150, 150, 150)
BLUE = (0, 0, 255)  # Default circle color

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

# Function to display text on screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def spawn_circle(circles, min_distance, circle_size):
    for _ in range(100):
        x = random.randint(circle_size, 1000 - circle_size)
        y = random.randint(circle_size, 800 - circle_size)
        new_circle = (x, y)
        if all((x - cx) ** 2 + (y - cy) ** 2 > (min_distance + circle_size) ** 2 for cx, cy in circles):
            return new_circle
    return None

def game(difficulty, circle_size, game_time, circle_color):
    print(f"Starting game with difficulty '{difficulty}', circle size '{circle_size}', and time '{game_time}' seconds")
    running = True
    score = 0
    start_time = time.time()
    circle_spawn_rate = {'easy': 0.02, 'medium': 0.03, 'hard': 0.04}[difficulty]
    disappearance_times = {'easy': 0.9 * 2, 'medium': 0.6 * 2, 'hard': 0.3 * 2}[difficulty]
    min_distance = {'easy': 100, 'medium': 75, 'hard': 50}[difficulty]
    circles = []
    circle_timers = []
    
    while running:
        screen.fill(WHITE)
        elapsed_time = time.time() - start_time
        
        if random.random() < circle_spawn_rate:
            new_circle = spawn_circle(circles, min_distance, circle_size)
            if new_circle:
                circles.append(new_circle)
                circle_timers.append(time.time())
        
        for i, (circle, spawn_time) in enumerate(zip(circles, circle_timers)):
            if time.time() - spawn_time > disappearance_times:
                circles.pop(i)
                circle_timers.pop(i)
            else:
                pygame.draw.circle(screen, circle_color, circle, circle_size)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, circle in enumerate(circles):
                    if (x - circle[0])**2 + (y - circle[1])**2 <= circle_size**2:
                        circles.pop(i)
                        circle_timers.pop(i)
                        score += 1
                        pop_sound.play()  # Play popping sound when circle is clicked
                        break
        
        draw_text(f'Time: {int(game_time - elapsed_time)}', font, BLACK, screen, 100, 30)
        draw_text(f'Score: {score}', font, BLACK, screen, 100, 70)
        
        if elapsed_time >= game_time:
            running = False
        
        pygame.display.flip()
        pygame.time.delay(10)
    
    return score

def show_summary(score, game_time):
    screen.fill(DARK_GREY)
    draw_text("Game Over", title_font, WHITE, screen, 500, 100)
    draw_text(f"Score: {score}", font, WHITE, screen, 500, 250)
    draw_text(f"Time: {game_time} seconds", font, WHITE, screen, 500, 300)
    
    pygame.draw.rect(screen, BLACK, pygame.Rect(400, 400, 200, 50))
    draw_text("Continue", font, WHITE, screen, 500, 425)
    
    pygame.display.flip()
    
    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 400 <= x <= 600 and 400 <= y <= 450:
                    waiting_for_click = False

def main_menu():
    selected_difficulty = None
    selected_size = None
    selected_time = None
    selected_color = None

    difficulty_options = {
        'easy': (200, 150, 20, BLACK),
        'medium': (400, 150, 20, BLACK),
        'hard': (600, 150, 20, BLACK)
    }
    
    size_options = {
        'small': (200, 300, 20, BLACK),
        'medium': (400, 300, 20, BLACK),
        'large': (600, 300, 20, BLACK)
    }

    time_options = {
        '30': (200, 450, 20, BLACK),
        '60': (400, 450, 20, BLACK),
        '120': (600, 450, 20, BLACK)
    }
    
    color_options = {
        'blue': (200, 600, 20, BLUE),
        'red': (400, 600, 20, (255, 0, 0)),
        'green': (600, 600, 20, (0, 255, 0))
    }
    
    while True:
        screen.fill(WHITE)
        
        draw_text("Aim Trainer", title_font, BLACK, screen, 500, 50)
        
        draw_text("Select Difficulty", font, BLACK, screen, 500, 120)
        for difficulty, (x, y, radius, color) in difficulty_options.items():
            pygame.draw.circle(screen, color, (x, y), radius, 0 if selected_difficulty == difficulty else 2)
            draw_text(difficulty.capitalize(), font, BLACK, screen, x, y + 40)
        
        draw_text("Select Circle Size", font, BLACK, screen, 500, 270)
        for size, (x, y, radius, color) in size_options.items():
            pygame.draw.circle(screen, color, (x, y), radius, 0 if selected_size == size else 2)
            draw_text(size.capitalize(), font, BLACK, screen, x, y + 40)
        
        draw_text("Select Game Time", font, BLACK, screen, 500, 420)
        for time, (x, y, radius, color) in time_options.items():
            pygame.draw.circle(screen, color, (x, y), radius, 0 if selected_time == time else 2)
            draw_text(f'{time} s', font, BLACK, screen, x, y + 40)
        
        draw_text("Select Circle Color", font, BLACK, screen, 500, 570)
        for color_name, (x, y, radius, color) in color_options.items():
            pygame.draw.circle(screen, color, (x, y), radius, 0 if selected_color == color else 2)
            draw_text(color_name.capitalize(), font, BLACK, screen, x, y + 40)
        
        if selected_difficulty and selected_size and selected_time:
            pygame.draw.rect(screen, BLACK, pygame.Rect(400, 700, 200, 50))
            draw_text("Start", font, WHITE, screen, 500, 725)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                for difficulty, (cx, cy, radius, color) in difficulty_options.items():
                    if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                        selected_difficulty = difficulty
                        print(f"Selected difficulty: {selected_difficulty}")
                
                for size, (cx, cy, radius, color) in size_options.items():
                    if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                        selected_size = size
                        print(f"Selected size: {selected_size}")
                
                for time, (cx, cy, radius, color) in time_options.items():
                    if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                        selected_time = time
                        print(f"Selected time: {selected_time} seconds")
                
                for color_name, (cx, cy, radius, color) in color_options.items():
                    if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                        selected_color = color
                        print(f"Selected color: {color_name.capitalize()}")
                
                if selected_difficulty and selected_size and selected_time and \
                   400 <= x <= 600 and 700 <= y <= 750:
                    try:
                        screen.fill(WHITE)
                        pygame.display.flip()
                        score = game(selected_difficulty, {'small': 10, 'medium': 20, 'large': 30}[selected_size], int(selected_time), selected_color)
                        show_summary(score, selected_time)
                    except Exception as e:
                        print(f"Error during game: {e}")
                    selected_difficulty = None
                    selected_size = None
                    selected_time = None
                    selected_color = BLUE

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"Error in main menu: {e}")
    finally:
        pygame.quit()