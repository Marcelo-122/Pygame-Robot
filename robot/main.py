import pygame, asyncio
import math

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paper Turtle Simulation")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Color for the trail
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)

# Robot parameters
robot_pos = [WIDTH // 2, HEIGHT // 2]  # Initial position at the center of the screen
robot_orientation = 0  # Initial orientation in radians
robot_speed = 0  # Speed of the robot
wheel_radius = 10
wheel_distance = 50  # Distance between wheels

# Speed limit
max_speed = 5  # Maximum speed the robot can go

# Control parameters
speed_increment = 1  # Speed adjustment factor
turn_increment = 0.1  # Turning adjustment factor

# Trail (to simulate the paper turtle trail)
trail = []

# Font for displaying coordinates
font = pygame.font.SysFont('Arial', 20)

# Button properties
button_rect = pygame.Rect(WIDTH - 160, 20, 140, 40)  # Position and size of the clear button
button_text = font.render("Limpa td", True, BLACK)

def draw_robot():
    # Calculate the end point for the orientation line (to show robot direction)
    orientation_end = (
        robot_pos[0] + 20 * math.cos(robot_orientation),
        robot_pos[1] + 20 * math.sin(robot_orientation)
    )
    
    # Draw robot as a blue circle and orientation line
    pygame.draw.circle(win, BLUE, (int(robot_pos[0]), int(robot_pos[1])), 15)
    pygame.draw.line(win, BLACK, robot_pos, orientation_end, 2)

def display_coordinates():
    # Render the x and y coordinates as text
    text = font.render(f"X: {int(robot_pos[0])} Y: {int(robot_pos[1])}", True, RED)
    win.blit(text, (10, 10))

def draw_trail():
    # Draw the trail
    for i in range(1, len(trail)):
        pygame.draw.line(win, GREEN, trail[i-1], trail[i], 2)

def draw_button():
    # Draw the button
    pygame.draw.rect(win, BUTTON_COLOR, button_rect)  # Draw button
    win.blit(button_text, (button_rect.x + 10, button_rect.y + 10))  # Draw button text

def check_button_click(mouse_pos):
    # Check if the mouse click is within the button area
    if button_rect.collidepoint(mouse_pos):
        return True
    return False

# Simulation loop
async def main():
    global robot_speed, robot_orientation, robot_pos, trail  # Declare globals
    running = True
    while running:
        # Frame rate
        pygame.time.delay(30)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button clicked
                    if check_button_click(event.pos):
                        trail.clear()  # Clear the trail

        # Key handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:  # Move forward
            robot_speed += speed_increment
        if keys[pygame.K_DOWN]:  # Move backward
            robot_speed -= speed_increment
        if keys[pygame.K_LEFT]:  # Turn left
            robot_orientation -= turn_increment
        if keys[pygame.K_RIGHT]:  # Turn right
            robot_orientation += turn_increment

        # Limit the speed to the maximum value
        if robot_speed > max_speed:
            robot_speed = max_speed
        elif robot_speed < -max_speed:
            robot_speed = -max_speed

        # Update robot position based on orientation and speed
        robot_pos[0] += robot_speed * math.cos(robot_orientation)
        robot_pos[1] += robot_speed * math.sin(robot_orientation)

        # Keep the robot within the screen boundaries
        if robot_pos[0] < 15:  # Prevent the robot from going out of bounds on the left
            robot_pos[0] = 15
        elif robot_pos[0] > WIDTH - 15:  # Prevent the robot from going out of bounds on the right
            robot_pos[0] = WIDTH - 15

        if robot_pos[1] < 15:  # Prevent the robot from going out of bounds on the top
            robot_pos[1] = 15
        elif robot_pos[1] > HEIGHT - 15:  # Prevent the robot from going out of bounds on the bottom
            robot_pos[1] = HEIGHT - 15

        # Add the current position to the trail
        trail.append(tuple(robot_pos))

        # Fill the background
        win.fill(WHITE)

        # Draw the trail, robot, and button
        draw_trail()
        draw_robot()
        draw_button()

        # Display the robot's coordinates
        display_coordinates()

        # Update display
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())
# Quit Pygame
pygame.quit()

