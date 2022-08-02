import pygame
import numpy as np
import time

class Fourier():

	def __init__(self, pts_x, pts_y, width, height, num_coeff):
		self.pts_x = pts_x
		self.pts_y = pts_y
		self.width = width
		self.height = height
		self.num_points = len(pts_x)
		self.num_coeff = num_coeff
		self.cfs = self.coefficients(pts_x, pts_y, num_coeff)
		self.complete_trace = self.calculate_serie(self.cfs, self.num_points)
		self.point = [0,0]
		self.trace = []

	def coefficients(self, pts_x, pts_y, number_coeff):
		wo = 2* np.pi
		num_points = len(pts_x)
		h = number_coeff // 2
		cfs = {}

		for n in range(-h, h + 1):
			cn = 0

			for iw in range(num_points):
				w = (iw/num_points)
				fw = complex(pts_x[iw], pts_y[iw])

				cn += fw * np.exp(1j * n * w * wo)

			cn /= num_points

			cfs[n] = cn

		order_cfs = dict(sorted(cfs.items(), key=lambda item: abs(item[1]), reverse=True))

		return order_cfs

	def calculate_serie(self, cfs, num_points):
		wo = 2 * np.pi

		points = []
		for it in range(num_points):
			t = (it/num_points)
			suma = 0

			for (n,cn) in (cfs.items()):
				suma += cn * np.exp(1j * wo * t * n)

			points.append([suma.real, suma.imag])

		return np.array(points)

	def draw_series_2(self, WIN, frame, vel, length_trace):
		wo = 2 * np.pi

		time.sleep(vel)

		frame = frame % self.num_points

		t = frame/self.num_points

		suma = 0

		radios = []
		centros = []

		for (n,cn) in (self.cfs.items()):
			suma += cn * np.exp(1j * wo * t * n)

			centros.append(suma)
			radios.append(abs(cn))

		self.point = [suma.real, suma.imag]

		#Draw all the figure in the background
		pygame.draw.lines(WIN, (49, 11, 11 ), False, self.complete_trace)

		#Draw border lines trace
		self.trace.insert(0, self.point)

		if length_trace >= self.num_points:
			length_trace = self.num_points - 10

		if len(self.trace) >= length_trace:
			self.trace.pop()

		num_sub_sections = 4
		section_trace = length_trace // num_sub_sections

		for i in range(num_sub_sections):
			sub_trace = self.trace[i * section_trace: section_trace * (i+1) + 1]
			if len(sub_trace) >= 2:
				pygame.draw.lines(WIN, (255,55 *i,55*i), False, sub_trace)

		#Draw epycycles
		for i in range(len(radios)):
			if radios[i] > 5:
				pygame.draw.circle(WIN, (255, 251, 129), (centros[i].real, centros[i].imag), radios[i], 1)

		#Draw intermediate lines
		for i in range(len(centros) - 1):
			pygame.draw.line(WIN, (158, 255, 127), (centros[i].real, centros[i].imag), (centros[i + 1].real, centros[i + 1].imag))


