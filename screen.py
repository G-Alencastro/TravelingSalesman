import pygame 
from pygame.locals import *
from main import *
import matplotlib.pyplot as plt

def draw_pts(pts):
    for pt in pts:
        pygame.draw.circle(screen, (150, 70, 30), pt, 10)

def draw_links(pts, matrix):
    for i in range(len(matrix)-1):
        pygame.draw.line(screen, (255, 175, 125), pts[matrix[i]], pts[matrix[i-1]], 3)
    pygame.draw.line(screen, (255, 175, 125), pts[matrix[-2]], pts[matrix[-1]], 3)

pygame.init()

screen_size = (900, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Traveling Saleman')

n_points = 20
pts = [(randint(10, 890), randint(0, 590)) for _ in range(n_points)]
pop = Population(1000, n_points)

gen = 0
fps = 1
clock = pygame.time.Clock()
while True:
    clock.tick(fps)
    screen.fill((230, 150, 100))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                fps += 1
            if event.key == K_DOWN:
                fps -= 1
        if event.type == QUIT:
            pygame.quit()


    pop.fit_pop(pts)
    print(gen)
    gen += 1
    draw_links(pts, pop.individuals[0].genome)
    draw_pts(pts)
    pop.new_population()


    pygame.display.update()
