import pygame
from random import choice

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10  # Adjust the radius according to the power-up icon size
        self.vel = 3  # Adjust the velocity of the power-up falling
        self.colors = {
            "extra_ball": (0, 255, 0),  # Color for the extra ball power-up
            "longer_paddle": (255, 0, 0)  # Color for the longer paddle power-up
        }
        self.color = choice(list(self.colors.values()))  # Randomly choose the color
        self.type = choice(["extra_ball", "longer_paddle"])  # Randomly choose the power-up type

    def draw(self, screen):
        pygame.draw.circle(screen, self.colors[self.type], (self.x, self.y), self.radius)

    def move(self):
        self.y += self.vel

    def check_collision(self, obj):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius).colliderect(obj)

    def activate(self, game):
        if self.type == "extra_ball":
            # Add logic to spawn extra balls
            pass
        elif self.type == "longer_paddle":
            # Add logic to activate a longer paddle
            pass
