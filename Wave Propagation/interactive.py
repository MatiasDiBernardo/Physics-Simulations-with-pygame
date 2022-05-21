import pygame

class Button():
	def __init__(self, x, y, image, image_press, scale, offset):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.image_press = pygame.transform.scale(image_press, (int(width * scale), int(height * scale)))
		self.offset = offset
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()
		real_pos_x = pos[0] - self.offset

		#check mouseover and clicked conditions
		if self.rect.collidepoint((real_pos_x, pos[1])):
			surface.blit(self.image_press, (self.rect.x, self.rect.y))
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		else:
			surface.blit(self.image, (self.rect.x, self.rect.y))

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action

class Play_Pause():

	def __init__(self, x, y, image_play, image_play_press, image_pause,image_pause_press, scale, offset):
		width = image_play.get_width()  #Assume all images has the same size
		height = image_play_press.get_height()
		self.image_play = pygame.transform.scale(image_play, (int(width * scale), int(height * scale)))
		self.image_play_press = pygame.transform.scale(image_play_press, (int(width * scale), int(height * scale)))
		self.image_pause = pygame.transform.scale(image_pause, (int(width * scale), int(height * scale)))
		self.image_pause_press = pygame.transform.scale(image_pause_press, (int(width * scale), int(height * scale)))
		self.offset = offset
		self.rect = self.image_play.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.change = 0
		self.action = False

	def draw(self, surface):

		pos = pygame.mouse.get_pos()
		real_pos_x = pos[0] - self.offset

		#check mouseover and clicked conditions
		if self.change%2 == 0:
			surface.blit(self.image_play_press, (self.rect.x, self.rect.y))
			if self.rect.collidepoint((real_pos_x, pos[1])):
				surface.blit(self.image_play_press, (self.rect.x, self.rect.y))
				if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
					self.clicked = True
					self.change += 1
					self.action = True
		else:
			surface.blit(self.image_pause_press, (self.rect.x, self.rect.y))
			if self.rect.collidepoint((real_pos_x, pos[1])):
				surface.blit(self.image_pause_press, (self.rect.x, self.rect.y))
				if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
					self.clicked = True
					self.change += 1
					self.action = False


		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return self.action

class Loading():
	
	def __init__(self, x, y, image, scale, angle):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.x = x
		self.y = y
		self.angle = angle

	def draw(self, surf, vel):

		pos = (self.x, self.y)
		w, h = self.image.get_size()
		originPos = (w/2, h/2)
		# offset from pivot to center
		image_rect = self.image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
		offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

		# roatated offset from pivot to center
		rotated_offset = offset_center_to_pivot.rotate(-int(self.angle/vel))

		# roatetd image center
		rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

		# get a rotated image
		rotated_image = pygame.transform.rotate(self.image, int(self.angle/vel))
		rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

		# rotate and blit the image
		surf.blit(rotated_image, rotated_image_rect)


class Slider():
	def __init__(self, x, y, width, height):
		#Height and widht of the total slider, only vertical
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.slider = pygame.Rect(self.x + int(self.width * 0.45), self.y + self.height//4, self.width//10, self.height//2)

	def draw(self, surface):
		action = False
		pos_abs = pygame.mouse.get_pos()
		self.pos = [pos_abs[0] - 500, pos_abs[1]]

		pygame.draw.rect(surface, (125,125,125), self.slider)
		pygame.draw.line(surface, (255,255,255), (self.x, self.y  + self.height// 2),  (self.x + self.width, self.y + self.height//2))

		slider_move = pygame.Rect(self.x, self.y, self.width, self.height)

		if slider_move.collidepoint(self.pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True
				self.slider = pygame.Rect(self.pos[0], self.y + self.height//4, self.width//10, self.height//2)  #Aca cambiando pos[0] a las x se podrdia adaptar a acostado

		return action


	def slice_values(self,min_value,max_value):
		min_border = self.x
		max_border = self.x + self.width

		a = (max_value - min_value)/(max_border - min_border)  #Regresion lineal para tener una escala entre 0 y 1
		b = max_value - a * max_border

		vol_scale = a * self.pos[0] + b

		return vol_scale

	def x_pos(self):
		return self.pos[0]
