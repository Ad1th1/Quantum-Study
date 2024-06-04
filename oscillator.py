import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coupled Spring-Mass System Simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

mass_width, mass_height = 40, 20
spring_constant = 0.1
damping = 0.01

x1 = WIDTH // 2 - 200
x2 = WIDTH // 2
v1 = 0
v2 = 0

equilibrium_length_1 = 100
equilibrium_length_2 = 100
equilibrium_length_3 = 100

dt = 0.1

def draw_spring(screen, color, start_pos, end_pos, num_coils=20, width=2, amplitude=5):
    x1, y1 = start_pos
    x2, y2 = end_pos
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    angle = math.atan2(y2 - y1, x2 - x1)

    segment_length = length / (num_coils * 2)
    points = []

    for i in range(num_coils * 2 + 1):
        x = x1 + segment_length * i * math.cos(angle)
        y = y1 + segment_length * i * math.sin(angle)

        if i % 2 == 0:
            x += amplitude * math.sin(angle)
            y -= amplitude * math.cos(angle)
        else:
            x -= amplitude * math.sin(angle)
            y += amplitude * math.cos(angle)

        points.append((x, y))

    pygame.draw.lines(screen, color, False, points, width)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    force1 = -spring_constant * (x1 - equilibrium_length_1)
    force2 = -spring_constant * (x2 - x1 - equilibrium_length_2)
    force3 = -spring_constant * (WIDTH - x2 - equilibrium_length_3)

    net_force1 = force1 - force2
    net_force2 = force2 - force3

    v1 += (net_force1 - damping * v1) * dt
    v2 += (net_force2 - damping * v2) * dt
    x1 += v1 * dt
    x2 += v2 * dt

    screen.fill(WHITE)

    draw_spring(screen, BLACK, (0, HEIGHT // 2), (x1, HEIGHT // 2))
    draw_spring(screen, BLACK, (x1, HEIGHT // 2), (x2, HEIGHT // 2))
    draw_spring(screen, BLACK, (x2, HEIGHT // 2), (WIDTH, HEIGHT // 2))

    pygame.draw.rect(screen, RED, (int(x1) - mass_width // 2, HEIGHT // 2 - mass_height // 2, mass_width, mass_height))
    pygame.draw.rect(screen, BLUE, (int(x2) - mass_width // 2, HEIGHT // 2 - mass_height // 2, mass_width, mass_height))

    pygame.display.flip()

    pygame.time.delay(int(dt * 1000))

pygame.quit()
