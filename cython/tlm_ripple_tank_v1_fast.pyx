#
# tlm_ripple_tank_v1_fast.pyx  ( simulated the ripple tank behaviour as seen at http://www.falstad.com/ripple/ ) in Cython
#
# CopyRight 2020 by Lumachina Software @_°° Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)
#
from init_lib import *
add_path_to_lib('matrix')
from matrici_fast import newMatrix,newMatrix3D

import time
import pygame, sys
from pygame.locals import *
import itertools

cdef int XRES,YRES,RES
XRES,YRES,RES = 560,480,4

cdef int DIMX,DIMY
DIMX,DIMY = XRES//RES,YRES//RES

cdef double R = -0.5				# reflection coefficient
cdef double T =  0.5				# transmission coefficient

cdef int SLIT_X = 100*RES		# slit horizontal position
cdef int SLIT_APERTURE = 2*RES	# slit aperture
cdef int SLIT_TICK = RES		# slit tickness

cdef int Q = 4					# provare con Q=15 e 256

pygame.init()
cdef object screen = pygame.display.set_mode((XRES,YRES))
cdef object	s = pygame.Surface((RES,RES))	# the object surface of a dimension of RES x RES
cdef object r = s.get_rect()				# the 'pixel' at x,y

cdef terminate(double t, int ng):
	cdef double dt = time.time()-t
	print(f'Velocità :  {ng/dt} generazioni al secondo')			# stampa a console il numero di generazioni
	print(f'Terminato dopo {int(dt)} secondi')
	pygame.quit()
	sys.exit()

cdef list Reset3D(list c, int x, int y):
	c[x][y][0],c[x][y][1],c[x][y][2],c[x][y][3] = 0.0,0.0,0.0,0.0
	return c

cdef list SetNode(list INCIDENT, int x, int y):
	for k in range(4):
		INCIDENT[x//RES][y//RES][k] = Q/2
	return INCIDENT
		
cdef list Scatter(list SCATTERED, list INCIDENT):
	# Calculate scattered wave at node (x,y)
	cdef int x,y
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):	
		SCATTERED[x][y][0] = R*INCIDENT[x][y][0] + T*INCIDENT[x][y][1] + T*INCIDENT[x][y][2] + T*INCIDENT[x][y][3]
		SCATTERED[x][y][1] = T*INCIDENT[x][y][0] + R*INCIDENT[x][y][1] + T*INCIDENT[x][y][2] + T*INCIDENT[x][y][3]
		SCATTERED[x][y][2] = T*INCIDENT[x][y][0] + T*INCIDENT[x][y][1] + R*INCIDENT[x][y][2] + T*INCIDENT[x][y][3]
		SCATTERED[x][y][3] = T*INCIDENT[x][y][0] + T*INCIDENT[x][y][1] + T*INCIDENT[x][y][2] + R*INCIDENT[x][y][3]
		INCIDENT = Reset3D(INCIDENT,x,y) # reset incident wave at node (x,y)
	return SCATTERED

cdef list Connect(list SCATTERED, list INCIDENT):
	# Connect scattered incidents to scattered ones
	cdef int x,y
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):	
		if SCATTERED[x][y][0] > 0: INCIDENT[x][y-1][2] = SCATTERED[x][y][0]
		if SCATTERED[x][y][1] > 0: INCIDENT[x-1][y][3] = SCATTERED[x][y][1]
		if SCATTERED[x][y][2] > 0: INCIDENT[x][y+1][0] = SCATTERED[x][y][2]
		if SCATTERED[x][y][3] > 0: INCIDENT[x+1][y][1] = SCATTERED[x][y][3]		
		SCATTERED = Reset3D(SCATTERED,x,y)	# reset scattered wave at node (x,y)
	return INCIDENT

cdef list SumPulses(list INCIDENT, list PRESSURE):
	# Superimpose incident pulses at node (x,y)
	cdef int x,y
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):	
		PRESSURE[x][y] = 0.5*(INCIDENT[x][y][0] + INCIDENT[x][y][1] + INCIDENT[x][y][2] + INCIDENT[x][y][3])
	return PRESSURE

cdef DrawTLM(list PRESSURE):
	cdef int x,y
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):
		s.fill((0,0,(50+200*PRESSURE[x][y])%256))
		r.x,r.y = x*RES,y*RES										# get an object rectangle from the object surface and place it at position x,y
		screen.blit(s,r)															# link the object rectangle to the object surface
	pygame.display.flip()	# update the entire pygame display
	
cdef tuple UpdateTLM(list PRESSURE, list SCATTERED, list INCIDENT):
	# updating lattice using the Ripple Tank rule with Moore neighboroods
	SCATTERED = Scatter(SCATTERED,INCIDENT)		# scattering
	INCIDENT  = Connect(SCATTERED,INCIDENT)		# connection process
	PRESSURE  = SumPulses(INCIDENT,PRESSURE)	# superimpose pulses 
	return (PRESSURE,SCATTERED,INCIDENT)


cpdef run():

	cdef double v = 0.0
	cdef list PRESSURE,SCATTERED,INCIDENT
	PRESSURE  = newMatrix  (DIMX+1,DIMY+1,	v)	# pressure value at node (x,y)
	SCATTERED = newMatrix3D(DIMX+1,DIMY+1,4,v)	# reflected wave four components at node (x,y)
	INCIDENT  = newMatrix3D(DIMX+1,DIMY+1,4,v)	# incident wave four components at node (x,y)
	
	cdef double T = time.time()
	NG = 0

	while True:
	
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate(T,NG)
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE: 
					terminate(T,NG)
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					INCIDENT = SetNode(INCIDENT,event.pos[0],event.pos[1])	# aggiunge una perturbazione
		
		DrawTLM(PRESSURE)
		#DrawObstacles()
		PRESSURE,SCATTERED,INCIDENT = UpdateTLM(PRESSURE,SCATTERED,INCIDENT)
		
		pygame.display.set_caption(f'TLM Ripple Tank v.1 (c)2020 by Lumachina Software - @_°° GEN:{NG}')
		NG +=1

	terminate(T,NG)
