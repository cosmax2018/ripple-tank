#
# tlm_ripple_tank_v1.py  ( simulated the ripple tank behaviour as seen at http://www.falstad.com/ripple/ )
#
# CopyRight 2019 by Lumachina Software @_°° Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)
#
from init_lib import *
add_path_to_lib(('matrici',),False)
from matrici import newMatrix

import time
import pygame, sys
from pygame.locals import *
import itertools
from matrici import newMatrix,newMatrix3D
from config_tlmrippletank import *

PRESSURE  = newMatrix  (DIMX+1,DIMY+1)		# pressure value at node (x,y)
SCATTERED = newMatrix3D(DIMX+1,DIMY+1,4)	# reflected wave four components at node (x,y)
INCIDENT  = newMatrix3D(DIMX+1,DIMY+1,4)	# incident wave four components at node (x,y)

pygame.init()
screen = pygame.display.set_mode((XRES,YRES))
s = pygame.Surface((RES,RES))	# the object surface of a dimension of RES x RES
r = s.get_rect()				# the 'pixel' at x,y
		
def terminate(t,ng):
	dt = time.time()-t
	print(f'Velocità :  {ng/dt} generazioni al secondo')			# stampa a console il numero di generazioni
	print(f'Terminato dopo {int(dt)} secondi')
	pygame.quit()
	sys.exit()

def Reset(c,x,y):
	for k in range(4): c[x][y][k] = 0

def SetNode(x,y):
	for k in range(4): INCIDENT[x//RES][y//RES][k] = Q/2
		
def Scatter():
	# Calculate scattered wave at node (x,y)
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):	
		SCATTERED[x][y][0] = R*INCIDENT[x][y][0] + T*INCIDENT[x][y][1] + T*INCIDENT[x][y][2] + T*INCIDENT[x][y][3]
		SCATTERED[x][y][1] = T*INCIDENT[x][y][0] + R*INCIDENT[x][y][1] + T*INCIDENT[x][y][2] + T*INCIDENT[x][y][3]
		SCATTERED[x][y][2] = T*INCIDENT[x][y][0] + T*INCIDENT[x][y][1] + R*INCIDENT[x][y][2] + T*INCIDENT[x][y][3]
		SCATTERED[x][y][3] = T*INCIDENT[x][y][0] + T*INCIDENT[x][y][1] + T*INCIDENT[x][y][2] + R*INCIDENT[x][y][3]
		
		Reset(INCIDENT,x,y) # reset incident wave at node (x,y)

def Connect():
	# Connect scattered incidents to scattered ones
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):	
		if SCATTERED[x][y][0] > 0: INCIDENT[x][y-1][2] = SCATTERED[x][y][0]
		if SCATTERED[x][y][1] > 0: INCIDENT[x-1][y][3] = SCATTERED[x][y][1]
		if SCATTERED[x][y][2] > 0: INCIDENT[x][y+1][0] = SCATTERED[x][y][2]
		if SCATTERED[x][y][3] > 0: INCIDENT[x+1][y][1] = SCATTERED[x][y][3]
		
		Reset(SCATTERED,x,y)	# reset scattered wave at node (x,y)

def SumPulses():
	# Superimpose incident pulses at node (x,y)
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):	
		PRESSURE[x][y] = 0.5*(INCIDENT[x][y][0] + INCIDENT[x][y][1] + INCIDENT[x][y][2] + INCIDENT[x][y][3])

def DrawTLM():
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):
		s.fill((0,0,(50+200*PRESSURE[x][y])%256))
		r.x,r.y = x*RES,y*RES										# get an object rectangle from the object surface and place it at position x,y
		screen.blit(s,r)															# link the object rectangle to the object surface
	
	pygame.display.flip()	# update the entire pygame display
	
def UpdateTLM():
	# updating lattice using the Ripple Tank rule with Moore neighboroods
	Scatter()		# scattering
	Connect()		# connection process
	SumPulses()		# superimpose pulses 


def main():

	t = time.time()
	NG = 0

	while time.time() - t < MAXTIME:
	
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate(t,NG)
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE: 
					terminate(t,NG)
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					SetNode(event.pos[0],event.pos[1])	# aggiunge una perturbazione
		
		DrawTLM()
		#DrawObstacles()
		UpdateTLM()
		
		pygame.display.set_caption(f'TLM Ripple Tank v.1 (c)2019 by Lumachina Software - @_°°           GEN:{NG}')
		NG +=1

	terminate(t,NG)

main()