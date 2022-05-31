import pygame 
import objects
import pandas as pd

WIDTH = 600
HEIGHT = 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

paredes1 = [[50,20,420,35], [480,450,250,490], [450,120,453,320], [50,450,250,480], [50, 150, 60, 366]]
paredes2 =[[30, 30, 450,35],[450,35,430,240],[430,240,450,450],[450,450,30,460],[30,460,30,30]]

walls = objects.Walls(paredes1)
fuente = objects.Source(250,300,360,50, WIDTH, HEIGHT, walls)

def main():
	run = True
	while run:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		WIN.fill((0,0,0))
		fuente.draw(WIN, (0,255,0), 270)
		walls.draw(WIN, (255,255,255))
		pygame.display.update()

	pygame.quit()

main()
