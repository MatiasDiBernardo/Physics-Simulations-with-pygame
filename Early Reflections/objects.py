import numpy as np
import pygame

class Walls():
	def __init__(self, pos):
		self.pos_walls = pos

	def draw(self, surface, color_line):
		for cord in self.pos_walls:
			pygame.draw.line(surface, color_line,(cord[0], cord[1]), (cord[2], cord[3]), width=2)

class Source():
	def __init__(self, x, y,angle_range, num_rays, width, height, class_walls):
		self.x1 = x
		self.y1 = y
		self.angle_range = angle_range
		self.num_rays = num_rays
		self.w = width
		self.h = height
		self.pos_walls = class_walls.pos_walls

	def draw(self, surface, color_line, des):
		angulos = np.linspace(0, self.angle_range, self.num_rays)

		pos_mouse = pygame.mouse.get_pos()

		x_circ = pos_mouse[0] 
		y_circ = pos_mouse[1]
		r = 10

		pygame.draw.circle(surface, (255,255,0), (x_circ, y_circ), r, 1)

		for omega in angulos:
			x1 = np.cos((omega + des) * (2*np.pi/360)) * self.w
			y1 = np.sin((omega + des) * (2*np.pi/360)) * self.h

			self.x2 = x1 + self.x1
			self.y2 = y1 + self.y1

			inter = self.intersection(self.x1, self.y1, self.x2, self.y2, 0)
			inter_circle = self.circle_intersection(self.x1, self.y1, self.x2, self.y2, x_circ, y_circ, r)
			self.draw_ray(inter_circle, surface, 1)

			if len(inter) != 0:  #First ray reflection
				self.x2 = inter[0]
				self.y2 = inter[1]

				self.x3, self.y3 = self.all_reflections(inter, self.x1, self.y1)

				inter2 = self.intersection(self.x2, self.y2, self.x3, self.y3, inter[2])
				inter_circle = self.circle_intersection(self.x2, self.y2, self.x3, self.y3, x_circ, y_circ, r)
				self.draw_ray(inter_circle, surface, 2)

				if len(inter2) != 0:  
					self.x3 = inter2[0]
					self.y3 = inter2[1]

					self.x4, self.y4 = self.all_reflections(inter2, self.x2, self.y2)

					inter3 = self.intersection(self.x3, self.y3, self.x4, self.y4, inter2[2])
					inter_circle = self.circle_intersection(self.x3, self.y3, self.x4, self.y4, x_circ, y_circ, r)
					self.draw_ray(inter_circle, surface, 3)

					if len(inter3) != 0:
						self.x4 = inter3[0]
						self.y4 = inter3[1]

						self.x5, self.y5 = self.all_reflections(inter3, self.x3, self.y3)

						inter4 = self.intersection(self.x4, self.y4, self.x5, self.y5, inter3[2])
						inter_circle = self.circle_intersection(self.x4, self.y4, self.x5, self.y5, x_circ, y_circ, r)
						self.draw_ray(inter_circle, surface, 4)

						if len(inter4) != 0:
							self.x5 = inter4[0]
							self.y5 = inter4[1]


	def intersection(self, x1, y1, x2, y2, current_wall):
		for wall in self.pos_walls:

			if wall == current_wall:
				continue
			x3 = wall[0]
			y3 = wall[1]
			x4 = wall[2]
			y4 = wall[3]

			num1 = (x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)
			num2 = (x1-x3)*(y1-y2) - (y1-y3)*(x1-x2)
			den  = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)

			if den == 0:  #If denominator = 0, parallel line 
				return []

			t = num1/den
			u = num2/den

			if t > 0 and t < 1 and u > 0 and u < 1:
				x_inter = x1 + t*(x2-x1)
				y_inter = y1 + t*(y2-y1)

				return [x_inter, y_inter, wall]

		return []

	def reflection(self, m_ray, wall, x1, y1, x2, y2):

		if wall[2] - wall[0] != 0:
			m_wall = (wall[3] - wall[1])/(wall[2] - wall[0])
		else:
			m_wall = (wall[3] - wall[1])/(0.01)

		angle = np.arctan((m_wall - m_ray)/(1 + m_wall*m_ray))

		if angle < 0 and self.inter_sector(x1, y1, x2, y2) == 2:
			angle += np.pi * 3/2

		if angle > 0 and self.inter_sector(x1, y1, x2, y2) == 2:
			angle -= np.pi/2

		if angle < 0 and self.inter_sector(x1, y1, x2, y2) == 1:
			angle -= np.pi/2

		if angle < 0 and self.inter_sector(x1, y1, x2, y2) == 3:
			angle += 3/2 * np.pi

		if angle > 0 and self.inter_sector(x1, y1, x2, y2) == 3:
			angle += np.pi

		if angle > 0 and self.inter_sector(x1, y1, x2, y2) == 4:
			angle += np.pi/2

		if self.inter_sector(x1, y1, x2, y2) == 0:
			angle += np.pi/2

		x_ref = np.cos(angle) * self.w * 5
		y_ref = np.sin(angle) * self.h * 5

		return [x_ref, y_ref]

	def inter_sector(self, x1, y1, x2, y2):  #Postion in cartesian plane of the intersction
		if x2 > x1 and y2 < y1:
			return 1
		if x2 < x1 and y2 < y1:
			return 2
		if x2 < x1 and y2 > y1:
			return 3
		if x2 > self.x1 and y2 > y1:
			return 4
		return 0

	def all_reflections(self, inter, x1, y1):
		if len(inter) != 0:
			x2 = inter[0]
			y2 = inter[1]

			if (x2 - x1) == 0:
				m_ray = (y2-y1)/0.001
			else:
				m_ray = (y2-y1)/(x2-x1)

			intercepted_wall = inter[2]
			pos_reflect = self.reflection(m_ray, intercepted_wall, x1, y1, x2, y2)
			x3 = pos_reflect[0] + x2
			y3 = pos_reflect[1] + y2

			return x3, y3

		else:
			return 0,0

	def circle_intersection(self, x1, y1, x2, y2, cir_X, cir_Y, cir_R):
		d = [x2-x1, y2-y1]
		f = [x1-cir_X, y1-cir_Y]

		a = np.dot(d,d)
		b = 2* np.dot(f,d)
		c = np.dot(f,f) - cir_R**2

		distriminant = b**2-4*a*c

		if distriminant > 0:
			t = (-b - np.sqrt(distriminant))/(2*a)

			x_inter = x1 + t * d[0]
			y_inter = y1 + t * d[1]

			return [x_inter, y_inter]
		else:
			return []
	
	def line_boundrie(self, x1, y1, x2, y2, c1, c2):

		horizontal = False
		vertical = False

		if x1 < x2 and c1 > x1 and c1 < x2:
			vertical = True
		if y1 < y2 and c2 > y1 and c2 < y2:
			horizontal = True
		if x1 > x2 and c1 < x1 and c1 > x2:
			vertical = True
		if y1 > y2 and c2 < y1 and c2 > y2:
			horizontal = True

		if horizontal or vertical:
			return True
		else:
			return False

	def draw_ray(self, inter_circle, surface, ray):

		color_line1 = (184, 6, 23)
		color_line2 = (145, 6, 184)
		color_line3 = (16, 83, 199)
		color_line4 = (25, 166, 72)

		if len(inter_circle) != 0 and self.line_boundrie(self.x1, self.y1, self.x2, self.y2, inter_circle[0], inter_circle[1]) and ray==1:
			self.x2 = inter_circle[0]
			self.y2 = inter_circle[1]

			pygame.draw.line(surface, color_line1,(self.x1, self.y1), (self.x2, self.y2), width=2)

		if len(inter_circle) != 0 and self.line_boundrie(self.x2, self.y2, self.x3, self.y3, inter_circle[0], inter_circle[1]) and ray==2:
			self.x3 = inter_circle[0]
			self.y3 = inter_circle[1]

			pygame.draw.line(surface, color_line2,(self.x1, self.y1), (self.x2, self.y2), width=2)
			pygame.draw.line(surface, color_line2,(self.x2, self.y2), (self.x3, self.y3), width=2)

		if len(inter_circle) != 0 and self.line_boundrie(self.x3, self.y3, self.x4, self.y4, inter_circle[0], inter_circle[1]) and ray==3:
			self.x4 = inter_circle[0]
			self.y4 = inter_circle[1]

			pygame.draw.line(surface, color_line3,(self.x1, self.y1), (self.x2, self.y2), width=2)
			pygame.draw.line(surface, color_line3,(self.x2, self.y2), (self.x3, self.y3), width=2)
			pygame.draw.line(surface, color_line3,(self.x3, self.y3), (self.x4, self.y4), width=2)

		if len(inter_circle) != 0 and self.line_boundrie(self.x4, self.y4, self.x5, self.y5, inter_circle[0], inter_circle[1]) and ray==4:
			self.x5 = inter_circle[0]
			self.y5 = inter_circle[1]

			pygame.draw.line(surface, color_line4,(self.x1, self.y1), (self.x2, self.y2), width=2)
			pygame.draw.line(surface, color_line4,(self.x2, self.y2), (self.x3, self.y3), width=2)
			pygame.draw.line(surface, color_line4,(self.x3, self.y3), (self.x4, self.y4), width=2)
			pygame.draw.line(surface, color_line4,(self.x4, self.y4), (self.x5, self.y5), width=2)
