import pygame
import random
import math
import pygame.gfxdraw

# Constants
PREDATOR_VISION = 40
PREDATOR_SPEED = 4
HUNGER_LIMIT = 600

class Predator:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.pos = pygame.math.Vector2(random.uniform(0, width), random.uniform(0, height))
        self.vel = self._get_random_velocity()
        self.max_speed = PREDATOR_SPEED
        self.radius = 7
        self.color = pygame.Color(163, 67, 67, 200)
        self.eaten = 0
        self.hunger = HUNGER_LIMIT

    def _get_random_velocity(self):
        angle = random.uniform(0, 2 * math.pi)
        magnitude = random.uniform(2, PREDATOR_SPEED)
        return pygame.math.Vector2(math.cos(angle), math.sin(angle)) * magnitude

    def _handle_boundary_collision(self):
        if self.pos.x > self.width:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = self.width
        if self.pos.y > self.height:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = self.height

    def _hunt(self, preys):
        closest_prey = None
        min_distance = PREDATOR_VISION

        for prey in preys:
            distance = self.pos.distance_to(prey.pos)
            if distance < min_distance:
                closest_prey = prey
                min_distance = distance

        if closest_prey:
            self.acc = (closest_prey.pos - self.pos).normalize() * self.max_speed - self.vel
        else:
            self.acc = pygame.math.Vector2()

    def _reproduce(self, predators):
        new_predator = Predator(self.screen, self.width, self.height)
        predators.append(new_predator)
        self.eaten = 0

    def eat_prey(self, predators):
        self.hunger = HUNGER_LIMIT
        self.eaten += 1
        if self.eaten >= 5:
            self._reproduce(predators)

    def update(self, preys):
        self._hunt(preys)
        self.vel += self.acc
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        self.pos += self.vel
        self._handle_boundary_collision()
        self.hunger -= 1

    def draw(self):
        angle = math.atan2(self.vel.y, self.vel.x)
        p1 = self.pos + pygame.math.Vector2(math.cos(angle), math.sin(angle)) * (self.radius * 2)
        p2 = self.pos + pygame.math.Vector2(math.cos(angle + 2.5), math.sin(angle + 2.5)) * (self.radius * 2)
        p3 = self.pos + pygame.math.Vector2(math.cos(angle - 2.5), math.sin(angle - 2.5)) * (self.radius * 2)

        pygame.gfxdraw.aapolygon(self.screen, [p1, p2, p3], self.color)
        pygame.gfxdraw.filled_polygon(self.screen, [p1, p2, p3], self.color)
