import os
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode([WIDTH,HEIGHT])
fps = 60
timer = pygame.time.Clock()

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
bird_models = [bird1,bird2]


class Spike:
    def __init__(self, x, y, model):
        self.x_coord = x
        self.y_coord = y
        self.model = model


for i in range(0,10):
    lspikes.append(Spike(wall_thickness, wall_thickness + i * 96, spike1))
for j in range(0,10):
    rspikes.append(Spike(WIDTH-wall_thickness-96, wall_thickness + j * 96, spike2))


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
        if self.y_pos < HEIGHT - 68 - (wall_thickness/2):
            self.y_speed += gravity
        else:
            if self.y_speed > bounce_stop:
                self.y_speed = self.y_speed * -1 * 0.9
            else:
                if abs(self.y_speed) <= bounce_stop:
                    self.y_speed = 0
        return self.y_speed

    def check_xpos(self):
        if self.x_pos < 0 + (wall_thickness/2):
            self.x_speed = self.x_speed * -1
        if self.x_pos > WIDTH - 80 - (wall_thickness/2):
            self.x_speed = self.x_speed * -1

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


run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    walls = draw_walls()
    player.move()
    for spike in lspikes:
        screen.blit(spike.model, (spike.x_coord, spike.y_coord))
    for spike in rspikes:
        screen.blit(spike.model, (spike.x_coord, spike.y_coord))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        player.y_speed = -10
    pygame.display.flip()
pygame.quit()
