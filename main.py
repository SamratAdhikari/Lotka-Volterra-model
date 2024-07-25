import pygame
from prey import Prey
from predator import Predator

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Constants
BG = (236, 242, 255)
GREY = (200, 200, 200)
RED = (163, 67, 67)
BLUE = (102, 123, 198)
FPS = 60
WIDTH, HEIGHT = pygame.display.get_surface().get_size()

N_PREYS = 200
N_PREDATORS = 50
MIN_PREYS = 10
MIN_PREDATORS = 5
PREY_REPRODUCTION_RATE = 0.5
REPRODUCTION_INTERVAL = 5000  # milliseconds

# Stats screen
stats_width = WIDTH // 10
stats_height = WIDTH // 8
stats = pygame.Surface((stats_width, stats_height))
stats.fill(GREY)
stats.set_alpha(200)
stats_pos = (WIDTH - stats_width - WIDTH // 40, HEIGHT // 40)

# Initialize populations
preys = [Prey(screen, WIDTH, HEIGHT) for _ in range(N_PREYS)]
predators = [Predator(screen, WIDTH, HEIGHT) for _ in range(N_PREDATORS)]

# Timer
reproduction_timer = pygame.time.get_ticks()

def ensure_population():
    """Ensure populations meet minimum thresholds."""
    if len(preys) < MIN_PREYS:
        preys.extend(Prey(screen, WIDTH, HEIGHT) for _ in range(MIN_PREYS - len(preys)))
    if len(predators) < MIN_PREDATORS:
        predators.extend(Predator(screen, WIDTH, HEIGHT) for _ in range(MIN_PREDATORS - len(predators)))

def check_collisions():
    """Handle collisions between predators and preys."""
    for predator in predators:
        for prey in preys[:]:
            if predator.pos.distance_to(prey.pos) < (predator.radius + prey.radius):
                preys.remove(prey)
                predator.eat_prey(predators)

def draw_stats_graph():
    """Draw the population statistics graph."""
    n_preys_now = len(preys)
    n_predators_now = len(predators)

    max_population = max(n_preys_now, n_predators_now, 1)
    stats.fill(GREY)
    bar_width = stats_width // 4
    max_bar_height = stats_height - 40

    prey_bar_height = int((n_preys_now / max_population) * max_bar_height)
    predator_bar_height = int((n_predators_now / max_population) * max_bar_height)

    # Draw bars
    pygame.draw.rect(stats, BLUE, (stats_width // 4 - bar_width // 2, stats_height - prey_bar_height - 20, bar_width, prey_bar_height))
    pygame.draw.rect(stats, RED, (3 * stats_width // 4 - bar_width // 2, stats_height - predator_bar_height - 20, bar_width, predator_bar_height))

    # Draw numbers
    font = pygame.font.SysFont(None, 24)
    prey_text = font.render(f'{n_preys_now}', True, BLUE)
    stats.blit(prey_text, (stats_width // 4 - prey_text.get_width() // 2, stats_height - prey_bar_height - 40))
    
    predator_text = font.render(f'{n_predators_now}', True, RED)
    stats.blit(predator_text, (3 * stats_width // 4 - predator_text.get_width() // 2, stats_height - predator_bar_height - 40))

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

    screen.fill(BG)
    check_collisions()

    # Update and draw all preys
    for prey in preys:
        prey.update(predators)
        prey.draw()

    # Update and draw all predators
    for predator in predators[:]:
        predator.update(preys)
        if predator.hunger <= 0:
            predators.remove(predator)
        predator.draw()

    # Handle prey reproduction
    current_time = pygame.time.get_ticks()
    if current_time - reproduction_timer >= REPRODUCTION_INTERVAL and preys:
        preys.extend(Prey(screen, WIDTH, HEIGHT) for _ in range(int(len(preys) * PREY_REPRODUCTION_RATE)))
        reproduction_timer = current_time

    ensure_population()

    draw_stats_graph()
    screen.blit(stats, stats_pos)

    pygame.display.flip()
    clock.tick(FPS)
