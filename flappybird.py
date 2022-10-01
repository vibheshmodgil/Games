import pygame
from pygame.locals import *
import random

pygame.init()

screen_width = 860
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#loading background image
bg = pygame.image.load('/Users/pratikkumarrana/Downloads/flappy_bird-main/img/bg.png')
#loading ground image
ground_img = pygame.image.load('/Users/pratikkumarrana/Downloads/flappy_bird-main/img/ground.png')
#loading button image
button_img = pygame.image.load('/Users/pratikkumarrana/Downloads/flappy_bird-main/img/restart.png')
#defining game variables
scroll_speed = 2
ground_pos = 0
run = True
fly = False
bird_alive = True
pipe_freq = 2000
time_last_pipe = pygame.time.get_ticks() - pipe_freq
pipe_gap = 170
counter = 0
bird_in_between = False
initial_disp = True

#font formatting
red = (255, 0, 0)
white = (255, 255, 255)
font_type1 = pygame.font.SysFont('Bauhaus 93', 60, True, False)
font_type2 = pygame.font.SysFont('Arial', 35, True, False)

#class for game reset button
class button():
    def __init__(self, x, y, button_img):
        self.image = button_img
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]

    def draw(self):
        action = False
        #getting mouse hovering position
        position = pygame.mouse.get_pos()  #returns x and y coordinate of the cursor
        if self.rect.collidepoint(position) and (pygame.mouse.get_pressed()[0]):
            action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

#reset function
def reset_game():
    pipe_group.empty()
    flappy.rect.center = [150, (screen_height//2)]
    score = 0
    return score


#function to convert text to image for score
def text2img(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

#Defining Bird Class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.time_counter = 0
        self.img_index = 0
        for i in range(1,4):
            img = pygame.image.load('/Users/pratikkumarrana/Downloads/flappy_bird-main/img/bird{}.png'.format(i))
            self.images.append(img)
        self.image = self.images[self.img_index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if (self.time_counter>12 and self.img_index<3):
            self.img_index += 1
            self.time_counter = 0
        if (self.img_index>2):
            self.img_index = 0
        self.time_counter += 1
        self.image = self.images[self.img_index]

    #adding game physics
        if (fly):
            #gravity
            if (self.vel<4):
                self.vel += 0.5
            else:
                self.vel = 0

            if self.rect.bottom <650:
                self.rect.y += int(self.vel)

        #Mouse-click action
        if ((pygame.mouse.get_pressed()[0]==1) and (self.clicked == False)):
            self.vel -= 10
            self.clicked = True
        if (pygame.mouse.get_pressed()[0] == 0):
            self.clicked = False

        #Rotate the bird
        self.image = pygame.transform.rotate(self.images[self.img_index], -2*self.vel)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('/Users/pratikkumarrana/Downloads/flappy_bird-main/img/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.rect.topleft = [x,y]
        if position == -1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y]

    def update(self):
        #for pipe scrolling
        self.rect.left -= scroll_speed
        if (self.rect.right<0):
            self.kill()

pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
flappy = Bird(150, (screen_height//2))
bird_group.add(flappy)
Button = button((screen_width//2 - 30), (screen_height//2 - 10), button_img)


while(run):
    time_now = pygame.time.get_ticks()
    screen.blit(bg, (0,0))
    pipe_group.draw(screen)
    screen.blit(ground_img, (ground_pos, 650))

    # Game end condition
    if (pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or (flappy.rect.top < 0)):
        bird_alive = False

    if (flappy.rect.bottom > 649):
        bird_alive = False
        fly = False
        flappy.image = pygame.transform.rotate(flappy.images[1], -90)

    #code for scrolling ground and pipe creation
    if ((bird_alive) and (fly)):
        ground_pos -= scroll_speed
        if ground_pos<-44:
            ground_pos = 0
        if (abs(time_now - time_last_pipe) > pipe_freq):
            pipe_height = random.randint(-150, 150)
            bottom_pipe = Pipe(screen_width, ((screen_height // 2) + (pipe_gap / 2) + pipe_height), 1)
            top_pipe = Pipe(screen_width, ((screen_height // 2) - (pipe_gap / 2) + pipe_height), -1)
            pipe_group.add(top_pipe)
            pipe_group.add(bottom_pipe)
            time_last_pipe = time_now

    bird_group.draw(screen)
    if (fly):
        bird_group.update()
    if (bird_alive):
        pipe_group.update()

    # score
    if len(pipe_group):
        if ((bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left) \
                and (bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right) \
                    and bird_in_between == False):
            bird_in_between = True
        if (((bird_group.sprites()[0].rect.left) > (pipe_group.sprites()[0].rect.right)) and (bird_in_between == True)):
            counter += 1
            bird_in_between = False
    text2img(('SCORE: ' + str(counter)), font_type1, red, (screen_width/2 - 60), 25)

    #game start or hard exit by user ('x' button pressed)
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False
        if ((events.type == pygame.MOUSEBUTTONDOWN) and (fly==False)):
            fly = True
            initial_disp = False
    if (initial_disp):
        text2img('Hi Pratik, Click to begin', font_type2, white, 270, 60)
    if (bird_alive==False):
        if(Button.draw()):
            counter = reset_game()
            bird_alive = True
    pygame.display.update()
pygame.quit()
