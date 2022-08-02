import pygame 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from objects import Fourier


WIDTH = 500
HEIGHT = 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

data_pi = np.genfromtxt('pi.csv',delimiter=',')

x_pi = data_pi[:,0]
y_pi = data_pi[:,1]


#Normalize the input data before pass it to the object (center the figure)

x_pi = (np.array(x_pi/2) - np.mean(x_pi/2) + WIDTH/2)
y_pi = (HEIGHT/2 - np.array(y_pi/2) - np.mean(y_pi/2) + 20)

number_coefficients = 15

draw_object = Fourier(x_pi, y_pi, WIDTH, HEIGHT, number_coefficients)

def main():
	global draw_object

	frame = 0
	run = True
	while run:
		clock.tick(25)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		WIN.fill((0,0,0))

		frame += 1

		draw_object.draw_series_2(WIN, frame, 0.05, 60)

		pygame.display.update()
	pygame.quit()


if __name__ == "__main__":
	main()