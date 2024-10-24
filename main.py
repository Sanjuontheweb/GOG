import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Guardians of the Galaxy')

# game variables
ground_scroll = 0
scroll_speed = 4

#load images
bg = pygame.image.load('imgs/bg.jpg')

class Shooter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img = pygame.image.load(f'imgs/roket{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):

        # handle the animation
        self.counter += 1
        counter_cooldown = 4

        if self.counter > counter_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

roket_group = pygame.sprite.Group()

movee = Shooter(int(screen_width // 2), 500)
roket_group.add(movee)

run = True
while run:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #make the roket movable
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            movee.rect.x -= 2
        elif event.key == pygame.K_RIGHT:
            movee.rect.x += 2

    # Clear the screen
    screen.fill((0, 0, 0))

    #draw the bg
    screen.blit(bg, (0, ground_scroll))

    #drawing the roket
    roket_group.draw(screen)
    roket_group.update()

    #scroll the bg
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 50:
        ground_scroll = 0

    pygame.display.update()

pygame.quit()