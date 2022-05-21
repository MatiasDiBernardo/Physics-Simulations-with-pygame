import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import numba


def draw_line(mat, x0, y0, x1, y1, inplace=False):
    if not (0 <= x0 < mat.shape[0] and 0 <= x1 < mat.shape[0] and
            0 <= y0 < mat.shape[1] and 0 <= y1 < mat.shape[1]):
        raise ValueError('Invalid coordinates.')
    if not inplace:
        mat = mat.copy()
    if (x0, y0) == (x1, y1):
        mat[x0, y0] = 2
        return mat if not inplace else None
    # Swap axes if Y slope is smaller than X slope
    transpose = abs(x1 - x0) < abs(y1 - y0)
    if transpose:
        mat = mat.T
        x0, y0, x1, y1 = y0, x0, y1, x1
    # Swap line direction to go left-to-right if necessary
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    # Write line ends
    mat[x0, y0] = 0
    mat[x1, y1] = 0
    # Compute intermediate coordinates using line equation
    x = np.arange(x0 + 1, x1)
    y = np.round(((y1 - y0) / (x1 - x0)) * (x - x0) + y0).astype(x.dtype)
    # Write intermediate coordinates
    mat[x, y] = 0
    if not inplace:
        return mat if not transpose else mat.T


def wave(source_location, walls_all, time, frec):

	#Wall horizontal [[x1,y1,x2,y2], misma lista con otra pared]

	nx   = 500          # number of grid points in x-direction
	nz   = nx           # number of grid points in z-direction
	dx   = 1.           # grid point distance in x-direction
	dz   = dx           # grid point distance in z-direction
	c0   = 340.         # wave velocity in medium (m/s)
	isx  = source_location[0]          # source location in grid in x-direction
	isz  = source_location[1]          # source location in grid in z-direction
	nt   = time         # maximum number of time steps
	dt   = 0.0010       # time step
	f0   = frec # dominant frequency of the source (Hz)
	t0   = 2. / f0 # source time shift

	p    = np.zeros((nz, nx)) # p at time n (now)
	pold = np.zeros((nz, nx)) # p at time n-1 (past)
	pnew = np.zeros((nz, nx)) # p at time n+1 (present)
	d2px = np.zeros((nz, nx)) # 2nd space derivative of p in x-direction
	d2pz = np.zeros((nz, nx)) # 2nd space derivative of p in z-direction

	c    = np.zeros((nz, nx))
	c    = c + c0             # initialize wave velocity in model

	src  = np.zeros(nt + 1)
	time = np.linspace(0 * dt, nt * dt, nt)
	time2 = np.arange(0,nt*dt,dt)

	# 1st derivative of a Gaussian
	src  = -8. * (time - t0) * f0 * (np.exp(-1.0 * (4*f0) ** 2 * (time - t0) ** 2))
	p_time = []

	for it in range(nt):

		d2pz, d2px = calculation_wave(dx, dz, d2pz, d2px, p)

		pnew = 2 * p - pold + (c ** 2) * (dt ** 2) * (d2pz + d2px)
		
		pnew[isz, isx] = pnew[isz, isx] + src[it] / (dx * dz) * (dt ** 2) 
		
		pold, p = p, pnew
		
		for i in range(len(walls_all)):
			p = draw_line(p, walls_all[i][0],walls_all[i][1],walls_all[i][2],walls_all[i][3])

		a = p + abs(np.min(p))  #Amplitude difference between 0 y 1
		a /= np.max(a)

		p_time.append(a)

	data = np.array(p_time)

	return data

@numba.jit()
def calculation_wave(dx, dz, d2pz, d2px, p):

	for index in range(1,499):  #Assume symmetrical surface
		d2pz[:, index] = (p[:, index - 1] - 2 * p[:, index] + p[:, index + 1]) / dz ** 2
		d2px[index, :] = (p[index - 1, :] - 2 * p[index, :] + p[index + 1, :]) / dx ** 2

	return d2pz, d2px

