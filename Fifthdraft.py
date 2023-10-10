import pygame
import random
import sys
import ast


# Constants
GRID_SIZE = 50
GRID_CELL_SIZE = 10
GRID_WIDTH = GRID_SIZE * GRID_CELL_SIZE
GRID_HEIGHT = GRID_SIZE * GRID_CELL_SIZE
WHITE = (255, 255, 255)
MUD = 0
LAVA = 1
BLANK = 2
SPEEDER = 3
GRID_TYPES = [MUD, LAVA, BLANK, SPEEDER]
GRID_COLORS = [(139, 69, 19), (255, 0, 0), (255, 255, 255), (0, 255, 0)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH + 250, GRID_HEIGHT + 250))
pygame.display.set_caption("Grid Game")


# allows for the saved data to be recalled from the txt file
def load_saved_data():
    try:
        with open ("saved_data.txt", "r") as file:
            saved_data_str = file.read()
            saved_data = ast.literal_eval(saved_data_str)
            return saved_data
    except FileNotFoundError: 
        return None
    
saved_data = load_saved_data()

# Create the grid with random square types and set player and endpoint
grid = [[random.choice(GRID_TYPES) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
start_x, start_y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
end_x, end_y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)

while grid[start_y][start_x] != BLANK:
    start_x, start_y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)

while grid[end_y][end_x] != BLANK or (end_x == start_x and end_y == start_y):
    end_x, end_y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)

# Player position and starting stats
player_x, player_y = start_x, start_y
moves = 450
health = 200

# Health bar and moves tracker initials
health_bar_width = 200
health_bar_height = 20
health_bar_x = 10
health_bar_y = GRID_HEIGHT + 30
font = pygame.font.Font(None, 36)
moves_text_x = GRID_WIDTH - 40
moves_text_y = GRID_HEIGHT + 40

# Define clock to control game speed
clock = pygame.time.Clock()


# Keep track of visited cells in the current move
visited_cells = set()

# Save button
save_button = pygame.Rect(GRID_WIDTH + 20, GRID_HEIGHT - 10, 100, 50)
save_button_color = (0, 255, 0)
save_button_text = font.render("Save", True, (255, 255, 255))

# Load button 
load_button = pygame.Rect(GRID_WIDTH + 140, GRID_HEIGHT - 10, 100, 50)
load_button_color = (255, 0, 0)
load_button_text = font.render("Load", True, (255, 255, 255))



# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE: 
            # Window resizaing funtion
            screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            GRID_WIDTH, GRID_HEIGHT = event.w - 100, event.h - 100
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if save_button.collidepoint(event.pos):
                # Save data when the button is clicked
                with open("saved_data.txt", "w") as file:
                    file.write(str(saved_data))
                print("Data saved to saved_data.txt")
            elif load_button.collidepoint(event.pos):
            # Load data when the button is clicked
             loaded_data = load_saved_data()
             if loaded_data is not None:
                # Update game state with loaded data
                health = loaded_data["health"]
                moves = loaded_data["moves"]
                player_x, player_y = loaded_data["location"]
                end_x, end_y = loaded_data["endpoint"]
                grid = loaded_data["grid"]
                visited_cells.clear()  # Clear visited cells
                moves_text_x = GRID_WIDTH - 40
                moves_text_y = GRID_HEIGHT + 40
    
    #save within the while loop so that updated game stats save
    saved_data = {
     "health": health,
     "moves": moves,
     "location": (player_x, player_y),
     "endpoint": (end_x, end_y),
     "grid": grid
}

    # Handle player input
    keys = pygame.key.get_pressed()
    move_made = False

    if keys[pygame.K_UP] and player_y > 0:
        new_position = (player_x, player_y - 1)
        #if new_position not in visited_cells:
        player_y -= 1
        visited_cells.add(new_position)
        move_made = True

    elif keys[pygame.K_DOWN] and player_y < GRID_SIZE - 1:
        new_position = (player_x, player_y + 1)
        #if new_position not in visited_cells:
        player_y += 1
        visited_cells.add(new_position)
        move_made = True

    elif keys[pygame.K_LEFT] and player_x > 0:
        new_position = (player_x - 1, player_y)
        #if new_position not in visited_cells:
        player_x -= 1
        visited_cells.add(new_position)
        move_made = True

    elif keys[pygame.K_RIGHT] and player_x < GRID_SIZE - 1:
        new_position = (player_x + 1, player_y)
        #if new_position not in visited_cells:
        player_x += 1
        visited_cells.add(new_position)
        move_made = True


 # diagnol movement 
    if keys[pygame.K_1] and player_x > 0 and player_y > 0:
        new_position = (player_x -1 , player_y - 1)
        player_x -= 1
        player_y -= 1
        visited_cells.add(new_position)
        move_made = True
    elif keys[pygame.K_2] and player_x < GRID_SIZE - 1 and player_y > 0:
        new_position = (player_x + 1 , player_y - 1)
        player_x += 1
        player_y -= 1
        visited_cells.add(new_position)
        move_made = True
    elif keys[pygame.K_3] and player_x > 0 and player_y < GRID_SIZE - 1:
        new_position = (player_x - 1 , player_y + 1)
        player_x -= 1
        player_y += 1
        visited_cells.add(new_position)
        move_made = True
    elif keys[pygame.K_4] and player_x < GRID_SIZE - 1 and player_y < GRID_SIZE - 1:
        new_position = (player_x + 1 , player_y + 1)
        player_x += 1
        player_y += 1
        visited_cells.add(new_position)
        move_made = True
 
    if move_made:
        move_made = False

        # Update grid effects (you can add more effects here)
        grid_type = grid[player_y][player_x]
        if grid_type == MUD:
            moves -= 10
            health -= 5
        elif grid_type == LAVA:
            moves -= 50
            health -= 10
        elif grid_type == BLANK:
            moves -= 1
        elif grid_type == SPEEDER:
            health -= 5

    # Draw the grid and player
    screen.fill((0, 0, 0))  # Clear the screen
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, GRID_COLORS[grid[y][x]], (x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))
            pygame.draw.rect(screen, WHITE, (x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE), 1)  # Draw grid cell borders
    
    # Color of player and endpoint
    pygame.draw.rect(screen, (0, 0, 255), (player_x * GRID_CELL_SIZE, player_y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))
    pygame.draw.rect(screen, (128, 0, 128), (end_x * GRID_CELL_SIZE, end_y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))

    # Health bar and moves counter
    pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width * (health / 200), health_bar_height))
    moves_text = font.render(f"Moves: {moves}", True, (128, 0, 128))
    screen.blit(moves_text, (moves_text_x, moves_text_y))

    # Draw the save button
    pygame.draw.rect(screen, save_button_color, save_button)
    text_x = save_button.centerx - save_button_text.get_width() // 2
    text_y = save_button.centery - save_button_text.get_height() // 2
    screen.blit(save_button_text, (text_x, text_y))
    
    #Draw the Load button 
    pygame.draw.rect(screen, load_button_color, load_button)
    text_x = load_button.centerx - load_button_text.get_width() // 2
    text_y = load_button.centery - load_button_text.get_height() // 2
    screen.blit(load_button_text, (text_x, text_y))

     # Check for game over conditions
    if moves <= 0 or health <= 0:
        running = False
        print('Game Over')

    # Check for victory condition
    if player_x == end_x and player_y == end_y:
        print('You Win!')
        pygame.time.delay(2000)  # Delay for 2 seconds before exiting
        running = False

    # Update the display
    pygame.display.flip()

    # Control game speed
    clock.tick(20)  # Limit to 30 frames per second

# Game over
pygame.quit()
sys.exit()

