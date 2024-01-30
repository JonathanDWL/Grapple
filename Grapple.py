'''
Tutorial demonstrates how to create a game window with Python Pygame.

Any pygame program that you create will have this basic code
'''

import pygame
import sys


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.width = 30
        self.height = 30
        self.color = (255, 64, 64)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.ellipse(self.image, self.color, (0, 0, self.width, self.height), width=0)
        self.rect = self.image.get_rect(center = (x, y))
        self.deltax = 0
        self.deltay = 0
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def move(self):
        key = pygame.key.get_pressed()
        if(key[pygame.K_LEFT]):
            self.deltax -= 0.5
        if(key[pygame.K_RIGHT]):
            self.deltax += 0.5
        if(key[pygame.K_UP]):
            self.deltay -= 5
        if(not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and self.deltax != 0):
            self.deltax = (abs(self.deltax)-0.5) * abs(self.deltax)/self.deltax
        self.deltay += 0.5
        self.x += self.deltax
        self.y += self.deltay
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if(self.deltay > 10):
            self.deltay = 10
        if(self.deltax < -3):
            self.deltax = -3
        if(self.deltax > 3):
            self.deltax = 3
        print(self.deltax)

    def collideblock(self, object):
        if(pygame.sprite.collide_mask(self, object)):
            correct = [0, 0]
            amount = 0
            if(self.y < object.rect.centery - object.height/2):
                correct = [0, -1]
                amount = (self.y + self.height/2) - (object.rect.centery - object.height/2)
            elif(self.y > object.rect.centery + object.height/2):
                correct = [0, 1]
                amount = (object.rect.centery + object.height/2) - (self.y - self.height/2)
            if(self.x < object.rect.centerx - object.width/2):
                correct = [-1, 0]
                amount = (self.x + self.width/2) - (object.rect.centerx - object.width/2)
            elif(self.x > object.rect.centerx + object.width/2):
                correct = [1, 0]
                amount = (object.rect.centerx + object.width/2) - (self.x - self.width/2)
            self.x += correct[0] * amount
            self.y += correct[1] * amount
            self.deltax -= abs(correct[0]) * self.deltax
            self.deltay -= abs(correct[1]) * self.deltay
            self.rect.centerx = self.x
            self.rect.centery = self.y

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super(Block, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = (x, y))
        self.width = width
        self.height = height

# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grapple")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create clock to later control frame rate
clock = pygame.time.Clock()

player = Player(400, 300)

blocks = pygame.sprite.Group()
blocks.add(Block(400, 400, 100, 20, (75, 75, 120)))

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    screen.fill(WHITE)

    player.move()
    for block in blocks:
        player.collideblock(block)
    screen.blit(player.image, player.rect.topleft)

    blocks.draw(screen)

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()