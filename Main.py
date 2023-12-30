import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH,HEIGHT])
fps = 60
timer = pygame.time.Clock()

wall_thickness = 10
gravity = 0.7
bounce_stop = 0.3
lspikes = []
rspikes = []


class Spike:
    def __init__(self, a, b, c, color):
        self.a_coord = a
        self.b_coord = b
        self.c_coord = c
        self.color = color


for i in range(0,10):
    lspikes.append(Spike((wall_thickness,10+i*70),(wall_thickness,80+i*70),(wall_thickness+45,40+i*70),'yellow'))
for j in range(0,10):
    rspikes.append(Spike((WIDTH,10+j*70),(WIDTH,80+j*70),(WIDTH-45,40+j*70),'yellow'))


class Bird:
    def __init__(self, x_pos, y_pos, color, x_speed, y_speed):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = 30
        self.color = color
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.circle = ''

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    def check_gravity(self):
        if self.y_pos < HEIGHT - self.radius - (wall_thickness/2):
            self.y_speed += gravity
        else:
            if self.y_speed > bounce_stop:
                self.y_speed = self.y_speed * -1 * 0.9
            else:
                if abs(self.y_speed) <= bounce_stop:
                    self.y_speed = 0
        return self.y_speed

    def check_xpos(self):
        if self.x_pos < 0 + self.radius + (wall_thickness/2):
            self.x_speed = self.x_speed * -1
        if self.x_pos > WIDTH - self.radius - (wall_thickness/2):
            self.x_speed = self.x_speed * -1

    def update_pos(self):
        self.y_pos += self.y_speed
        self.x_pos += self.x_speed

    def move(self):
        self.draw()
        self.update_pos()
        self.check_gravity()
        self.check_xpos()


player = Bird(300, 300, 'green', 10, 0)

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
        pygame.draw.polygon(screen,spike.color,(spike.a_coord,spike.b_coord,spike.c_coord))
    for spike in rspikes:
        pygame.draw.polygon(screen, spike.color, (spike.a_coord, spike.b_coord, spike.c_coord))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        player.y_speed = -10
    pygame.display.flip()
pygame.quit()
