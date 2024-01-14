import os
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode([WIDTH,HEIGHT])
fps = 60
timer = pygame.time.Clock()

collision = False
wall_thickness = 10
gravity = 0.7
bounce_stop = 0.3
lspikes = []
rspikes = []
folder_path = os.path.join(os.path.dirname(__file__),'graphics')
spike1 = pygame.image.load(os.path.join(folder_path,'left_spike.png'))
spike2 = pygame.image.load(os.path.join(folder_path,'right_spike.png'))
bird1 = pygame.image.load(os.path.join(folder_path,'bird_left.png'))
bird2 = pygame.image.load(os.path.join(folder_path,'bird_right.png'))
background = pygame.image.load(os.path.join(folder_path, 'background.png'))
bird_models = [bird1,bird2]


class Spike:
    def __init__(self, x, y, model, speed):
        self.x_coord = x
        self.y_coord = y
        self.model = model
        self.speed = speed

    def move_spike(self):
        self.x_coord += self.speed


for i in range(0, 8):
    lspikes.append(Spike(wall_thickness - 2 - 100, wall_thickness + i * 116, spike1, 4))
for j in range(0, 8):
    rspikes.append(Spike(WIDTH-wall_thickness-92, wall_thickness + j * 116, spike2, 4))


class Bird:
    def __init__(self, x_pos, y_pos, x_speed, y_speed, models):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.models = models

    def draw(self):
        if self.x_speed > 0:
            screen.blit(self.models[1],(self.x_pos, self.y_pos))
        else:
            screen.blit(self.models[0],(self.x_pos, self.y_pos))

    def check_gravity(self):
        if self.y_pos < HEIGHT - 77 - (wall_thickness/2):
            self.y_speed += gravity
        else:
            if self.y_speed > bounce_stop:
                self.y_speed = self.y_speed * -1 * 0.9
            else:
                if abs(self.y_speed) <= bounce_stop:
                    self.y_speed = 0
        return self.y_speed

    def check_xpos(self):
        global move_counter
        global facing_left
        if self.x_pos < 0 + wall_thickness:
            self.x_speed = self.x_speed * -1
            for spike in lspikes:
                spike.speed *= -1
            for spike in rspikes:
                spike.speed *= -1
            move_counter = 0
            facing_left = True
        if self.x_pos > WIDTH - 80 - wall_thickness:
            self.x_speed = self.x_speed * -1
            for spike in rspikes:
                spike.speed *= -1
            for spike in lspikes:
                spike.speed *= -1
            move_counter = 0
            facing_left = False

    def update_pos(self):
        self.y_pos += self.y_speed
        self.x_pos += self.x_speed

    def move(self):
        self.draw()
        self.update_pos()
        self.check_gravity()
        self.check_xpos()


player = Bird(300, 300, 10, 0, bird_models)

def draw_walls():
    left = pygame.draw.line(screen, 'white', (0, 0), (0, HEIGHT), wall_thickness)
    right = pygame.draw.line(screen, 'white', (WIDTH, 0), (WIDTH, HEIGHT), wall_thickness)
    top = pygame.draw.line(screen, 'white', (0, 0), (WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(screen, 'white', (0, HEIGHT), (WIDTH, HEIGHT), wall_thickness)
    wall_list = [left,right,top,bottom]
    return wall_list

move_counter = 0
facing_left = False

run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    screen.blit(background, (0, 0))
    player.move()
    for spike in lspikes:
        if move_counter<464:
            if move_counter > 60:
                spike.move_spike()
            move_counter+=1
        screen.blit(spike.model, (spike.x_coord, spike.y_coord))
    for spike in rspikes:
        if move_counter<464:
            if move_counter > 60:
                spike.move_spike()
            move_counter+=1
        screen.blit(spike.model, (spike.x_coord, spike.y_coord))
    draw_walls()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.y_speed = -13
    pygame.display.flip()
pygame.quit()
