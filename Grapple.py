'''
Tutorial demonstrates how to create a game window with Python Pygame.

Any pygame program that you create will have this basic code
'''

import pygame
import sys
import math


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

    def move(self, grounded):
        key = pygame.key.get_pressed()
        if(key[pygame.K_LEFT]):
            self.deltax -= 0.5
        if(key[pygame.K_RIGHT]):
            self.deltax += 0.5
        if(key[pygame.K_UP] and grounded):
            self.deltay -= 10
        if(not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and self.deltax != 0):
            self.deltax = (abs(self.deltax)-0.5) * abs(self.deltax)/self.deltax
        self.deltay += 0.6
        self.x += self.deltax
        self.y += self.deltay
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if(self.deltay > 10):
            self.deltay = 10
        if(self.deltax < -4):
            self.deltax = -4
        if(self.deltax > 4):
            self.deltax = 4

    def collideblock(self, object):
        grounded = False
        if(pygame.sprite.collide_mask(self, object)):
            correct = [0, 0]
            if(self.y + self.height/2 > object.rect.centery - object.height/2 and self.y < object.rect.top):
                correct[1] = (object.rect.centery - object.height/2) - (self.y + self.height/2)
                grounded = True
            elif(self.y - self.height/2 < object.rect.centery + object.height/2 and self.y > object.rect.bottom):
                correct[1] = (object.rect.centery + object.height/2) - (self.y - self.height/2)
            if(self.x + self.width/2 > object.rect.centerx - object.width/2 and self.x < object.rect.left):
                correct[0] = (object.rect.centerx - object.width/2) - (self.x + self.width/2)
            elif(self.x - self.width/2 < object.rect.centerx + object.width/2 and self.x > object.rect.right):
                correct[0] = (object.rect.centerx + object.width/2) - (self.x - self.width/2)
            self.x += correct[0]
            self.y += correct[1]
            print(correct)
            self.deltax -= self.deltax * correct[0]/(self.width/2)
            self.deltay -= self.deltay * correct[1]/(self.width/2)
            self.rect.centerx = self.x
            self.rect.centery = self.y
        return(grounded)


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
blocks.add(Block(500, 375, 100, 70, (75, 75, 120)))

onground = False

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., white)
    screen.fill(WHITE)

    player.move(onground)
    onground = False
    for block in blocks:
        if(player.collideblock(block)):
            onground = True
    screen.blit(player.image, player.rect.topleft)

    blocks.draw(screen)

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()