#
# tlm_ripple_tank.py  ( simulated the ripple tank behaviour as seen at http://www.falstad.com/ripple/ )
#
# CopyRight 2019 by Lumachina Software @_°° Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)
#
from init_lib import *
add_path_to_lib('matrix')

import time
import pygame, sys
from pygame.locals import *
import itertools
from matrici import newArray
from config_tlmrippletank import *

class Node:
	def __init__(self,_pressure_,_scattered_,_incident_):
		self.PRESSURE  = _pressure_
		self.SCATTERED = _scattered_
		self.INCIDENT  = _incident_

global WAVE,NG
WAVE = []
for y in range(DIMX+1):
	row = []
	for x in range(DIMY+1):
		row.append(Node(0.0,newArray(4),newArray(4)))
	WAVE.append(row)

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

def Reset(c):
	for k in range(4): c[k] = 0

def SetNode(x,y):
	for k in range(4): WAVE[x//RES][y//RES].INCIDENT[k] = Q/2
		
def Scatter():
	# Calculate scattered wave at node (x,y)
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):	
			WAVE[x][y].SCATTERED[0] = R*WAVE[x][y].INCIDENT[0] + T*WAVE[x][y].INCIDENT[1] + T*WAVE[x][y].INCIDENT[2] + T*WAVE[x][y].INCIDENT[3]
			WAVE[x][y].SCATTERED[1] = T*WAVE[x][y].INCIDENT[0] + R*WAVE[x][y].INCIDENT[1] + T*WAVE[x][y].INCIDENT[2] + T*WAVE[x][y].INCIDENT[3]
			WAVE[x][y].SCATTERED[2] = T*WAVE[x][y].INCIDENT[0] + T*WAVE[x][y].INCIDENT[1] + R*WAVE[x][y].INCIDENT[2] + T*WAVE[x][y].INCIDENT[3]
			WAVE[x][y].SCATTERED[3] = T*WAVE[x][y].INCIDENT[0] + T*WAVE[x][y].INCIDENT[1] + T*WAVE[x][y].INCIDENT[2] + R*WAVE[x][y].INCIDENT[3]
			
			Reset(WAVE[x][y].INCIDENT) # reset incident wave at node (x,y)

def Connect():
	# Connect scattered incidents to scattered ones
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):	
		if WAVE[x][y].SCATTERED[0] > 0: WAVE[x][y-1].INCIDENT[2] = WAVE[x][y].SCATTERED[0]
		if WAVE[x][y].SCATTERED[1] > 0: WAVE[x-1][y].INCIDENT[3] = WAVE[x][y].SCATTERED[1]
		if WAVE[x][y].SCATTERED[2] > 0: WAVE[x][y+1].INCIDENT[0] = WAVE[x][y].SCATTERED[2]
		if WAVE[x][y].SCATTERED[3] > 0: WAVE[x+1][y].INCIDENT[1] = WAVE[x][y].SCATTERED[3]
		
		Reset(WAVE[x][y].SCATTERED)	# reset scattered wave at node (x,y)

def SumPulses():
	# Superimpose incident pulses at node (x,y)
	for x,y in itertools.product(range(1,DIMX),range(1,DIMY)):	
		WAVE[x][y].PRESSURE = 0.5*(WAVE[x][y].INCIDENT[0] + WAVE[x][y].INCIDENT[1] + WAVE[x][y].INCIDENT[2] + WAVE[x][y].INCIDENT[3])

def DrawTLM():
	for x,y in itertools.product(range(DIMX),range(DIMY)):
		s.fill((0,0,(50+200*WAVE[x][y].PRESSURE)%256))
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
		
		pygame.display.set_caption(f'TLM Ripple Tank (c)2019 by Lumachina Software - @_°°           GEN:{NG}')
		NG +=1

	terminate(t,NG)

main()