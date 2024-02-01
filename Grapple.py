'''
Tutorial demonstrates how to create a game window with Python Pygame.

Any pygame program that you create will have this basic code
'''

import pygame
import sys
import math

def sign(num):
    if(num == 0):
        return(0)
    else:
        return(abs(num)/num)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.width = 30
        self.height = 30
        self.widt = self.width
        self.heig = self.height
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
            self.deltax = (abs(self.deltax)-0.5) * sign(self.deltax)
            if(abs(self.deltax) < 0.1):
                self.deltax = 0
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
            yd = 0
            xd = 0
            if(self.rect.bottom > object.rect.top and self.y < object.rect.top):
                yd = self.y - object.rect.top
                grounded = True
            elif(self.rect.top < object.rect.bottom and self.y > object.rect.bottom):
                yd = self.y - object.rect.bottom
            if(self.rect.right > object.rect.left and self.x < object.rect.left):
                xd = self.x - object.rect.left
            elif(self.rect.left < object.rect.right and self.x > object.rect.right):
                xd = self.x - object.rect.right
            hd = (xd**2 + yd**2)**(1/2)
            if(xd != 0):
                th = math.atan(yd/xd)
            else:
                th = math.pi/2
            w = self.width/2
            h = self.height/2
            hyp = w*h/((h**2*math.cos(th)**2 + w**2*math.sin(th)**2)**(1/2))
            correct = [sign(xd)*abs((hyp-hd)*math.cos(th)), sign(yd)*abs((hyp-hd)*math.sin(th))]
            self.x += correct[0]
            self.y += correct[1]
            if(hyp-hd != 0):
                self.deltax -= self.deltax * abs(correct[0]/(hyp-hd))
                self.deltay -= self.deltay * abs(correct[1]/(hyp-hd))
            self.rect.centerx = self.x
            self.rect.centery = self.y
        return(grounded)
    
    def collidespike(self, object):
        if(pygame.sprite.collide_mask(self, object)):
            return(True)
        return(False)
    
    def squish(self, groundedlast):
        buffer = self.deltay
        if(groundedlast and self.deltax == 0):
            self.deltay = 0
        if(self.deltay != 0):
            wid = abs(30 * self.deltax/self.deltay)
        else:
            wid = 9999
        if(self.deltax != 0):
            hei = abs(30 * self.deltay/self.deltax)
        else:
            hei = 9999
        if(self.deltax == self.deltay):
            wid = 30
            hei = 30
        if(wid > 36):
            wid = 36
        elif(wid < 25):
            wid = 25
        if(hei > 36):
            hei = 36
        elif(hei < 25):
            hei = 25

        self.widt += (wid-self.widt)*0.2
        self.heig += (hei-self.heig)*0.2

        self.width = int(self.widt)
        self.height = int(self.heig)

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.ellipse(self.image, self.color, (0, 0, self.width, self.height), width=0)
        self.rect = self.image.get_rect(center = (self.x, self.y))

        self.deltay = buffer


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super(Block, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.width = width
        self.height = height

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super(Spike, self).__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.polygon(self.image, color, [(self.width/2, 0), (0, self.height), (self.width, self.height)], width=0)
        self.rect = self.image.get_rect(topleft = (x, y))


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

player = Player(50, 560)

blocks = pygame.sprite.Group()
blocks.add(Block(0, 0, 800, 25, (75, 75, 120)))
blocks.add(Block(0, 575, 800, 25, (75, 75, 120)))
blocks.add(Block(0, 0, 25, 600, (75, 75, 120)))
blocks.add(Block(775, 0, 25, 600, (75, 75, 120)))
blocks.add(Block(300, 525, 200, 100, (75, 75, 120)))
blocks.add(Block(0, 375, 700, 25, (75, 75, 120)))
blocks.add(Block(700, 500, 100, 25, (75, 75, 120)))
blocks.add(Block(600, 500, 50, 25, (75, 75, 120)))
blocks.add(Block(750, 425, 100, 25, (75, 75, 120)))

spikes = pygame.sprite.Group()
spikes.add(Spike(200, 550, 25, 25, (100, 100, 250)))
spikes.add(Spike(225, 550, 25, 25, (100, 100, 250)))
spikes.add(Spike(350, 500, 25, 25, (100, 100, 250)))
spikes.add(Spike(375, 500, 25, 25, (100, 100, 250)))
spikes.add(Spike(400, 500, 25, 25, (100, 100, 250)))
spikes.add(Spike(425, 500, 25, 25, (100, 100, 250)))
spikes.add(Spike(600, 475, 25, 25, (100, 100, 250)))
spikes.add(Spike(700, 475, 25, 25, (100, 100, 250)))

onground = False
ongroundlast = False

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
    kill = False
    for spike in spikes:
        if(player.collidespike(spike)):
            kill = True
    player.squish(ongroundlast)
    ongroundlast = onground
    if(kill):
        player.kill()
        player = Player(50, 560)
    screen.blit(player.image, player.rect.topleft)

    blocks.draw(screen)
    spikes.draw(screen)

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()