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
scroll_speed = 2.5
bug_frequency = 1000 # millisec
last_bug = pygame.time.get_ticks() - bug_frequency
game_over = False
rocking = False
score = 0

#load images
bg = pygame.image.load('imgs/bg.jpg')
start_img = pygame.image.load('imgs/start.png')
restart_img = pygame.image.load('imgs/restartt1.png')

def reset_game():
    bugs_group.empty()
    movee.rect.x = (screen_width / 2)

    score = 0
    return score

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

class Bugs(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for numb in range(1, 6):
            img = pygame.image.load(f'imgs/{numb}.png')
            self.images.append(img)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0

    def update(self):

        # scroll the bugs down
        self.rect.y += scroll_speed
        if pygame.sprite.spritecollide(movee, bugs_group, False):
            global game_over
            game_over = True
            self.kill()
            
        # handle the animation
        self.counter += 1
        counter_cooldown = 20

        if self.counter > counter_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

class Restart():
    def __init__(self, x, y):
            self.images = []  # List to hold images for animation
            for num in range(1, 3):
                img = pygame.image.load(f'imgs/restartt{num}.png')
                self.images.append(img)
            
            self.index = 0  # Current image index
            self.counter = 0  # Counter for animation timing
            self.cooldown = 45  # Timing for switching images
            self.image = self.images[self.index]  # Set the initial image
            self.rect = self.image.get_rect()  # Create the rect for the button
            self.rect.topleft = (x, y)  # Set the position of the button

    def draw(self):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # Update animation
        self.counter += 1
        if self.counter > self.cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]  # Update the image based on the index

        # Draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
    
class Start():
    def __init__(self, x, y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

roket_group = pygame.sprite.Group()
bugs_group = pygame.sprite.Group()

movee = Shooter(int(screen_width // 2), 540)
roket_group.add(movee)

restart_btn = Restart(0, 0)
start_btn = Start(0, 0, start_img)

run = True
while run:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if game_over == False and rocking == True:

        # make the roket movable
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            movee.rect.x -= 7
        elif keys[pygame.K_RIGHT]:
            movee.rect.x += 7

        # making the roket move inside the frame
        if movee.rect.x < 0:  # left boundary
            movee.rect.x = 0
        elif movee.rect.x > screen_width - movee.rect.width:  # right boundary
            movee.rect.x = screen_width - movee.rect.width

    if pygame.sprite.spritecollide(movee, bugs_group, False):
        game_over = True

    if game_over:
        if restart_btn.draw() == True:
            game_over = False
            score = reset_game()
            last_bug = pygame.time.get_ticks() - bug_frequency

    if game_over == False and rocking == True:
        time_now = pygame.time.get_ticks()
        bug_width = 38
        if time_now - last_bug > bug_frequency:
            top_bug = Bugs(random.randint(0, screen_width - bug_width), 0)
            bugs_group.add(top_bug)
            last_bug = time_now

    # Clear the screen
    screen.fill((0, 0, 0))

    #draw the bg
    screen.blit(bg, (0, 0))

    # updating the bugs
    bugs_group.update()

    # drawing the bugs
    bugs_group.draw(screen)

    #drawing the roket
    roket_group.draw(screen)
    roket_group.update()

    if game_over:
        restart_btn.draw()

    # Draw the start button if the game is not started
    if rocking == False and game_over == False:
        start_btn.draw()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                rocking = True  # Starting the game when clicked
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    rocking = True

    pygame.display.update()

pygame.quit()