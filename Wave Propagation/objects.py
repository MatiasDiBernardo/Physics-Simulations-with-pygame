import numpy as np
import pygame

class Speaker():
	def __init__(self, start_x, start_y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.x = start_x - self.width//2
		self.y = start_y - self.height//2
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.x, self.y)

	def draw(self, surface):
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				self.x, self.y = pos
				self.x = self.x - self.width//2
				self.y = self.y - self.height//2
				self.rect.topleft = (self.x, self.y)
				self.clicked = True

		surface.blit(self.image, (self.x, self.y))

	def position(self):
		acutual_x = self.x + self.width//2
		acutual_y = self.y + self.height//2
		return acutual_x, acutual_y

class Walls():
	def __init__(self):
		self.num_clicks = 0
		self.start_point_x = 0
		self.start_point_y = 0
		self.end_point_x = 0
		self.end_point_y = 0
		self.final_line = 0
		self.new = True

	def set_position(self, surface, click):

		pos = pygame.mouse.get_pos()
		color_circle = (255,255,255)
		color_line = (255,255,0)

		self.num_clicks = click

		if click == 0:
			pygame.draw.circle(surface, color_circle, pos, 5, 5)
			self.start_point_x = pos[0]
			self.start_point_y = pos[1]
			self.new = False

		if click == 1:
			pygame.draw.line(surface, color_line,(self.start_point_x, self.start_point_y), pos, width=2)
			self.end_point_x = pos[0]
			self.end_point_y = pos[1]

		if click == 2:
			self.final_line = pygame.draw.line(surface, color_line,(self.start_point_x, self.start_point_y), (self.end_point_x, self.end_point_y), width=2)

	def position(self):
		return [self.start_point_x,	self.start_point_y,self.end_point_x, self.end_point_y]

	def draw(self, surface):
		color_line = (255,255,0)
		if self.end_point_x != 0 and self.end_point_y !=0:
			pygame.draw.line(surface, color_line,(self.start_point_x, self.start_point_y), (self.end_point_x, self.end_point_y), width=2)
