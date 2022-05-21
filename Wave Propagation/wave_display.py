import pygame
from wave_generator import wave
import numpy as np
import objects
import interactive
import threading
pygame.font.init()

WIDTH = 500
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH + 150, HEIGHT))
ANIMATION = pygame.Surface((WIDTH, HEIGHT))
MENU = pygame.Surface((150, HEIGHT))

pygame.display.set_caption('Waves')

time = 700
frec = 25

wave_conditions = np.array([[250,250], [], time, frec], dtype=object)  #Pasar esto a numpy y cambiar en el codigo la parte de las paredes

#Load images and create the buttons

PLAY_IMAGE = pygame.image.load('images/play_button.png').convert_alpha()
PLAY_IMAGE_PRESS = pygame.image.load('images/play_button_press.png').convert_alpha()

PAUSE_IMAGE = pygame.image.load('images/pause.png').convert_alpha()
PAUSE_IMAGE_PRESS = pygame.image.load('images/pause_press.png').convert_alpha()

SPEAKER_IMAGE = pygame.image.load('images/speaker.png').convert_alpha()
SPEAKER_IMAGE_PRESS = pygame.image.load('images/speaker_press.png').convert_alpha()

LOADING_IMAGE = pygame.image.load('images/loading.png').convert_alpha()

WALL_IMAGE = pygame.image.load('images/wall.png').convert_alpha()
WALL_IMAGE_PRESS = pygame.image.load('images/wall_press.png').convert_alpha()

ERASE_IMAGE = pygame.image.load('images/erase.png').convert_alpha()
ERASE_IMAGE_PRESS = pygame.image.load('images/erase_press.png').convert_alpha()

play_pause_button = interactive.Play_Pause(50, 415, PLAY_IMAGE, PLAY_IMAGE_PRESS, PAUSE_IMAGE, PAUSE_IMAGE_PRESS, 1, 500)
WALL_BUTTON = interactive.Button(50,40, WALL_IMAGE, WALL_IMAGE_PRESS, 1, 500)
ERASE_BUTTON = interactive.Button(50,152, ERASE_IMAGE, ERASE_IMAGE_PRESS, 1, 500)
LOADING = interactive.Loading(20,480, LOADING_IMAGE,0.15, 0)
frec_slider = interactive.Slider(20,270, 110,20)
time_slider = interactive.Slider(20,350, 110,20)
font = pygame.font.Font('images/AldotheApache.ttf', 16)
font2 = pygame.font.Font('images/AldotheApache.ttf', 12)


speaker = objects.Speaker(250,250, SPEAKER_IMAGE, 1)
speakers = [objects.Speaker(250,250, SPEAKER_IMAGE, 1)] #Tengo cambiar varias cosas para que funcionen los dos al mismo tiempo. no se si vale la pena

load = False

def loading():
	global load

	if not load:
		return True
	else:
		return False

def load_sound(wave_cond):
	global load
	global wave_use

	load = False
	wave_use = wave(wave_cond[0], wave_cond[1], wave_cond[2], wave_cond[3])
	load = True

def thread_loading_sound(values):
	global load

	x = threading.Thread(target=load_sound, args=(values,))
	x.start()

thread_loading_sound(wave_conditions)

def create_image(g, step):
	r = np.zeros((WIDTH, HEIGHT))
	b = np.ones((WIDTH, HEIGHT)) * 100
	rgb_uint8 = (np.dstack((r,g[step,:,:],b)) * 255.999).astype(np.uint8)

	return rgb_uint8

def main():
	global wave_conditions
	global wave_use
	global time
	global frec

	time = wave_conditions[2]
	forward = True
	step = 0 
	run = True
	all_walls = []
	click = 0

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click += 1

		if not loading():
			plot = create_image(wave_use, step)
		else:
			plot = np.zeros((WIDTH, HEIGHT))
		
		pygame.surfarray.blit_array(ANIMATION, plot)
		WIN.blit(ANIMATION, (0,0))
		WIN.blit(MENU, (500,0))
		MENU.fill((0,0,100))

		wall_text = font.render('Walls', True, (255,255,255))
		MENU.blit(wall_text, (55,10))
		erase_text = font.render('Erase', True, (255,255,255))
		MENU.blit(erase_text, (56,125))
		frec_text = font.render('Frecueny', True, (255,255,255))
		MENU.blit(frec_text, (45,235))
		time_text = font.render('Time', True, (255,255,255))
		MENU.blit(time_text, (58,320))

		if frec_slider.draw(MENU):
			frec = round(frec_slider.slice_values(20,200))
			frec_actual_text = font2.render(str(frec), True, (255,255,255))
			x_pos = frec_slider.x_pos()
			MENU.blit(frec_actual_text,(x_pos, 258))

		if time_slider.draw(MENU):
			time = round(time_slider.slice_values(1,20))
			time_actual_text = font2.render(str(time), True, (255,255,255))
			x_pos_t = time_slider.x_pos()
			MENU.blit(time_actual_text,(x_pos_t, 340))
			time *= 100

		if play_pause_button.draw(MENU):
			if np.any(wave_conditions != new_wave_condition):
				thread_loading_sound(new_wave_condition)
				wave_conditions = np.copy(new_wave_condition)

			if forward:
				step += 1
				if step > time - 2:
					forward = False
			else:
				step -= 1
				if step < 1:
					forward = True

		if WALL_BUTTON.draw(MENU) and not play_pause_button.draw(MENU):
			wall = objects.Walls()
			all_walls.append(wall)

		if ERASE_BUTTON.draw(MENU):
			all_walls = []
			plot = np.zeros((WIDTH, HEIGHT))
			step = 0

		if len(all_walls) != 0:  #Aca entra a revisar esto siempre, si quiero lo cambio pero asi funciona
			if wall.new:
				click = 0
			wall.set_position(WIN, click)

		if loading():
			LOADING.draw(WIN,3)
			LOADING.angle += 1
			step = 0

		if not loading():
			cordinates_walls = []

			for i in range(len(all_walls)):
				all_walls[i].draw(WIN)
				cords = all_walls[i].position()
				cordinates_walls.append(cords)

			speaker.draw(WIN)
			new_x, new_y = speaker.position()
			new_wave_condition = np.array([[new_y,new_x], cordinates_walls, time, frec], dtype=object)

		pygame.display.update()

	pygame.quit()
	
main()