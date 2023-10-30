import pygame
import math

pygame.init()

# Constants
G = 6.67430e-11
mass1 = 100000000000  # Arbitrary mass of the star (larger particle)
mass2 = 1  # Mass of the planet
time_step = 1

# Colors
WHITE = (254, 255, 185)
RED = (210, 43, 43)
BLUE = (13, 135, 145)

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Orbital Simulation")

# Particle properties
particle1_radius = 20
particle1_color = RED
particle2_radius = 10
particle2_color = BLUE

# Initial positions
particle1_x = screen_width // 2
particle1_y = screen_height // 2
particle2_x = particle1_x + 100
particle2_y = particle1_y + 100

# Initial velocities (start the simulation with good parameters!)
particle1_vx = 0
particle1_vy = 0
particle2_vx = -0.2
particle2_vy = -0.005

dragging_particle2 = False

# Set up the path tracker surface after defining screen dimensions
path_tracker = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
path_color = (0, 0, 255, 70)  # Light blue with transparency

# Create a list to store the positions of the smaller particle (fill initial array with the starting coordinates of particle 2)
path_positions = [[particle1_x + 100,particle1_y + 100],[particle1_x + 100,particle1_y + 100]]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if math.sqrt((mouse_x - particle2_x)**2 + (mouse_y - particle2_y)**2) < particle2_radius:
                dragging_particle2 = True

        if event.type == pygame.MOUSEBUTTONUP:
            dragging_particle2 = False

    if dragging_particle2:
        particle2_x, particle2_y = pygame.mouse.get_pos()
        
    # Check for collision
    if math.sqrt((particle2_x - particle1_x)**2 + (particle2_y - particle1_y)**2) <= (particle1_radius + particle2_radius):
        # Calculate new velocities after collision
        v1_final_x = ((mass1 - mass2) * particle1_vx + 2 * mass2 * particle2_vx) / (mass1 + mass2)
        v1_final_y = ((mass1 - mass2) * particle1_vy + 2 * mass2 * particle2_vy) / (mass1 + mass2)
        v2_final_x = ((mass2 - mass1) * particle2_vx + 2 * mass1 * particle1_vx) / (mass1 + mass2)
        v2_final_y = ((mass2 - mass1) * particle2_vy + 2 * mass1 * particle1_vy) / (mass1 + mass2)

        particle1_vx, particle1_vy = v1_final_x, v1_final_y
        particle2_vx, particle2_vy = v2_final_x, v2_final_y

   # Update particle positions
    delta_x = particle2_x - particle1_x
    delta_y = particle2_y - particle1_y
    distance = max(math.sqrt(delta_x**2 + delta_y**2), particle1_radius)

    force = G * (mass1 * mass2) / distance**2
    force_x = force * (delta_x / distance)
    force_y = force * (delta_y / distance)


    particle2_x += particle2_vx * time_step
    particle2_y += particle2_vy * time_step

    # Calculate the direction vector from particle2 to particle1
    direction_x = particle1_x - particle2_x
    direction_y = particle1_y - particle2_y

    # Calculate the distance between particle1 and particle2
    distance = math.sqrt(direction_x**2 + direction_y**2)

    # Calculate the gravitational force acting on particle2
    force = G * (mass1 * mass2) / distance**2
    force_x = force * (direction_x / distance)
    force_y = force * (direction_y / distance)

    acceleration_x = force_x / mass2
    acceleration_y = force_y / mass2

    particle2_vx += acceleration_x * time_step
    particle2_vy += acceleration_y * time_step
    
    # Update the path tracker surface
    path_positions.append([int(particle2_x), int(particle2_y)])
    path_tracker.fill((0, 0, 0, 0))  # Clear the path tracker
    pygame.draw.lines(path_tracker, path_color, False, path_positions, 2)  # Draw the path

    if len(path_positions) >= 2:
        pygame.draw.lines(path_tracker, path_color, False, path_positions, 2)  # Draw the path

    screen.fill(WHITE)

    screen.blit(path_tracker, (0, 0))

    pygame.draw.circle(screen, particle1_color, (particle1_x, particle1_y), particle1_radius)
    pygame.draw.circle(screen, particle2_color, (int(particle2_x), int(particle2_y),), particle2_radius)

    pygame.display.update()

pygame.quit()

