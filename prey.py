import pygame
import random
import math
import pygame.gfxdraw

# Constants
PREY_VISION = 70
PREY_SPEED = 2

class Prey:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.pos = pygame.math.Vector2(random.uniform(0, width), random.uniform(0, height))
        self.vel = self._get_random_velocity()
        self.max_speed = PREY_SPEED
        self.radius = 5
        self.color = pygame.Color(102, 123, 198, 200)

    def _get_random_velocity(self):
        angle = random.uniform(0, 2 * math.pi)
        magnitude = random.uniform(2, PREY_SPEED)
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

    def _flee(self, predators):
        steer = pygame.math.Vector2()
        total = 0
        
        for predator in predators:
            distance = self.pos.distance_to(predator.pos)
            if distance < PREY_VISION:
                diff = self.pos - predator.pos
                if distance > 0:
                    diff /= distance
                steer += diff
                total += 1

        if total > 0:
            steer /= total
            if steer.length() > 0:
                steer = steer.normalize() * self.max_speed - self.vel

        return steer

    def update(self, predators):
        self.acc = self._flee(predators)
        self.vel += self.acc
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        self.pos += self.vel
        self._handle_boundary_collision()

    def draw(self):
        angle = math.atan2(self.vel.y, self.vel.x)
        p1 = self.pos + pygame.math.Vector2(math.cos(angle), math.sin(angle)) * (self.radius * 2)
        p2 = self.pos + pygame.math.Vector2(math.cos(angle + 2.5), math.sin(angle + 2.5)) * (self.radius * 2)
        p3 = self.pos + pygame.math.Vector2(math.cos(angle - 2.5), math.sin(angle - 2.5)) * (self.radius * 2)

        pygame.gfxdraw.aapolygon(self.screen, [p1, p2, p3], self.color)
        pygame.gfxdraw.filled_polygon(self.screen, [p1, p2, p3], self.color)
