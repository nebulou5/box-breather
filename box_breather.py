import sys
import pygame
import argparse

# Initialize Pygame
pygame.init()

# Argument parsing with config file support
parser = argparse.ArgumentParser(description="Box Breather")
parser.add_argument("times", nargs="*", type=int, help="Animation times (1, 2, or 4 integers)")
parser.add_argument("--config", type=str, help="Path to config file")
args = parser.parse_args()

# Default values
LEG1_TIME = LEG2_TIME = LEG3_TIME = LEG4_TIME = 2
BACKGROUND_COLOR = (255, 255, 255)  # White
BOX_COLOR = (0, 0, 0)               # Black
CIRCLE_COLOR = (255, 0, 0)          # Red
BOX_WIDTH_PERCENT = 0.5
BOX_HEIGHT_PERCENT = 0.5
BOX_THICKNESS = 2
CIRCLE_START_RADIUS = 20.0
CIRCLE_END_RADIUS = CIRCLE_START_RADIUS * 3

# New optional parameter for text rendering inside the circle.
# It can be either False, True, or an RGB tuple.
DISPLAY_TEXT = False

# Load from config file if specified
if args.config:
    try:
        with open(args.config, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == 'leg1_time':
                    LEG1_TIME = int(value)
                elif key == 'leg2_time':
                    LEG2_TIME = int(value)
                elif key == 'leg3_time':
                    LEG3_TIME = int(value)
                elif key == 'leg4_time':
                    LEG4_TIME = int(value)
                elif key == 'background_color':
                    BACKGROUND_COLOR = tuple(map(int, value.split(',')))
                elif key == 'box_color':
                    BOX_COLOR = tuple(map(int, value.split(',')))
                elif key == 'circle_color':
                    CIRCLE_COLOR = tuple(map(int, value.split(',')))
                elif key == 'box_width_percent':
                    BOX_WIDTH_PERCENT = float(value)
                elif key == 'box_height_percent':
                    BOX_HEIGHT_PERCENT = float(value)
                elif key == 'box_thickness':
                    BOX_THICKNESS = int(value)
                elif key == 'circle_start_radius':
                    CIRCLE_START_RADIUS = float(value)
                elif key == 'circle_end_radius':
                    CIRCLE_END_RADIUS = float(value)
                elif key == 'display_text':
                    # Accept "false", "true", or an RGB value like "255,255,0"
                    if value.lower() == 'false':
                        DISPLAY_TEXT = False
                    elif value.lower() == 'true':
                        DISPLAY_TEXT = True
                    else:
                        try:
                            rgb = tuple(map(int, value.split(',')))
                            if len(rgb) == 3:
                                DISPLAY_TEXT = rgb
                            else:
                                raise ValueError("RGB must have 3 values")
                        except Exception as e:
                            print("Invalid display_text configuration value. Expected 'true', 'false', or an RGB value.")
                            sys.exit(1)
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)
elif args.times:
    if len(args.times) not in [1, 2, 4]:
        print("Usage: python script.py <seconds> [vertical_seconds] [leg2_seconds leg3_seconds] or --config=filename.txt")
        sys.exit(1)
    try:
        if any(t <= 0 for t in args.times):
            raise ValueError
        if len(args.times) == 1:
            LEG1_TIME = LEG2_TIME = LEG3_TIME = LEG4_TIME = args.times[0]
        elif len(args.times) == 2:
            LEG1_TIME = LEG3_TIME = args.times[0]
            LEG2_TIME = LEG4_TIME = args.times[1]
        else:
            LEG1_TIME, LEG2_TIME, LEG3_TIME, LEG4_TIME = args.times
    except ValueError:
        print("Please provide positive integers for seconds")
        sys.exit(1)

# Initial window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CURRENT_WIDTH = WINDOW_WIDTH
CURRENT_HEIGHT = WINDOW_HEIGHT
TARGET_WIDTH = WINDOW_WIDTH
TARGET_HEIGHT = WINDOW_HEIGHT

# Animation timing
FPS = 60
FRAME_TIME1 = LEG1_TIME * FPS
FRAME_TIME2 = LEG2_TIME * FPS
FRAME_TIME3 = LEG3_TIME * FPS
FRAME_TIME4 = LEG4_TIME * FPS
TOTAL_CYCLE = FRAME_TIME1 + FRAME_TIME2 + FRAME_TIME3 + FRAME_TIME4
RESIZE_SPEED = 0.1

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Box Breather")
clock = pygame.time.Clock()

def get_box_dimensions(current_size):
    box_width = int(current_size[0] * BOX_WIDTH_PERCENT)
    box_height = int(current_size[1] * BOX_HEIGHT_PERCENT)
    box_x = (current_size[0] - box_width) // 2
    box_y = (current_size[1] - box_height) // 2
    return box_x, box_y, box_width, box_height

def get_circle_position_and_radius(frame, box_x, box_y, box_width, box_height):
    # Compute the inset offset so the circle follows the center of the box's border
    offset = BOX_THICKNESS / 2
    current_frame = frame % TOTAL_CYCLE

    if current_frame < FRAME_TIME1:
        # Top horizontal: move from left+offset to right-offset at a constant y position
        t = current_frame / FRAME_TIME1
        x = box_x + offset + (box_width - 2 * offset) * t
        y = box_y + offset
        radius = CIRCLE_START_RADIUS + (CIRCLE_END_RADIUS - CIRCLE_START_RADIUS) * t
    elif current_frame < FRAME_TIME1 + FRAME_TIME2:
        # Right vertical: move from top+offset to bottom-offset at constant x position
        t = (current_frame - FRAME_TIME1) / FRAME_TIME2
        x = box_x + box_width - offset
        y = box_y + offset + (box_height - 2 * offset) * t
        radius = CIRCLE_END_RADIUS
    elif current_frame < FRAME_TIME1 + FRAME_TIME2 + FRAME_TIME3:
        # Bottom horizontal: move from right-offset to left+offset at constant y position
        t = (current_frame - FRAME_TIME1 - FRAME_TIME2) / FRAME_TIME3
        x = box_x + box_width - offset - (box_width - 2 * offset) * t
        y = box_y + box_height - offset
        radius = CIRCLE_END_RADIUS - (CIRCLE_END_RADIUS - CIRCLE_START_RADIUS) * t
    else:
        # Left vertical: move from bottom-offset to top+offset at constant x position
        t = (current_frame - FRAME_TIME1 - FRAME_TIME2 - FRAME_TIME3) / FRAME_TIME4
        x = box_x + offset
        y = box_y + box_height - offset - (box_height - 2 * offset) * t
        radius = CIRCLE_START_RADIUS

    return int(x), int(y), radius

# Main game loop
running = True
frame = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.VIDEORESIZE:
            TARGET_WIDTH, TARGET_HEIGHT = event.size
            screen = pygame.display.set_mode((TARGET_WIDTH, TARGET_HEIGHT), pygame.RESIZABLE)

    CURRENT_WIDTH += (TARGET_WIDTH - CURRENT_WIDTH) * RESIZE_SPEED
    CURRENT_HEIGHT += (TARGET_HEIGHT - CURRENT_HEIGHT) * RESIZE_SPEED

    box_x, box_y, box_width, box_height = get_box_dimensions((CURRENT_WIDTH, CURRENT_HEIGHT))

    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, BOX_COLOR, (box_x, box_y, box_width, box_height), BOX_THICKNESS)

    circle_x, circle_y, circle_radius = get_circle_position_and_radius(
        frame, box_x, box_y, box_width, box_height
    )
    pygame.draw.circle(screen, CIRCLE_COLOR, (circle_x, circle_y), circle_radius)

    # If display_text is enabled (True or an RGB tuple), render the remaining duration text
    if DISPLAY_TEXT:
        # Determine text color: use BOX_COLOR if DISPLAY_TEXT is True, otherwise use the RGB tuple
        text_color = BOX_COLOR if DISPLAY_TEXT is True else DISPLAY_TEXT
        
        # Compute the remaining frames and seconds for the current leg.
        current_cycle_frame = frame % TOTAL_CYCLE
        if current_cycle_frame < FRAME_TIME1:
            remaining_frames = FRAME_TIME1 - current_cycle_frame
        elif current_cycle_frame < FRAME_TIME1 + FRAME_TIME2:
            remaining_frames = FRAME_TIME1 + FRAME_TIME2 - current_cycle_frame
        elif current_cycle_frame < FRAME_TIME1 + FRAME_TIME2 + FRAME_TIME3:
            remaining_frames = FRAME_TIME1 + FRAME_TIME2 + FRAME_TIME3 - current_cycle_frame
        else:
            remaining_frames = TOTAL_CYCLE - current_cycle_frame
        remaining_seconds = round(remaining_frames / FPS)
        
        # Dynamically determine the font size as 1.2 of the current circle radius (with a minimum font size)
        dynamic_font_size = max(10, int(circle_radius * 1.2))
        font = pygame.font.Font(None, dynamic_font_size)
        text_surface = font.render(str(remaining_seconds), True, text_color)
        text_rect = text_surface.get_rect(center=(circle_x, circle_y))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    frame += 1
    clock.tick(FPS)

pygame.quit()
sys.exit(0)

