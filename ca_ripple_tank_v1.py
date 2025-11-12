#
# ca_ripple_tank_v1.py  ( simulated the ripple tank behaviour as seen at http://www.falstad.com/ripple/ )
#
# CopyRight 2019 by Lumachina Software @_°° Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)
#
# questa versione usa swapMatrix(a,b) e si comporta correttamente. 

from matrici import newMatrix

import time
import pygame, sys
from pygame.locals import *
import itertools
from config_carippletank import *

pygame.init()
screen = pygame.display.set_mode((XRES,YRES))
s = pygame.Surface((RES,RES))
r = s.get_rect()

def terminate(t,ng):
	dt = time.time()-t
	print(f'Velocità :  {ng/dt} generazioni al secondo')			# stampa a console il numero di generazioni
	print(f'Terminato dopo {int(dt)} secondi')
	pygame.quit()
	sys.exit()

def RippleTankRule(sx,cx,dx,up,dw,us,ds,ud,dd):
	# Implementing the Ripple Tank Machine
	floater = (sx+dx+up+dw+us+ds+ud+dd)/4-cx
	if floater < DECAY:
		return DECAY
	else:
		if floater > Q:
			return Q
		else:
			return floater - DECAY

def SetIC(IC,x,y):
	IC[x//RES][y//RES] = INTENSITY*Q
	return IC

def UpdateCA(CA,IC):
	# updating lattice using the Ripple Tank rule with Moore neighboroods
	for i,j in itertools.product(range(1,DIM[0]-1),range(1,DIM[1]-1)):
		xs,xc,xd,yu,yc,yd = (i-1,i,i+1,j+1,j,j-1) # stabilisce quali sono i vicini della cellula
		CA[i][j] =  RippleTankRule(IC[xs][yc],\
								  CA[xc][yc],\
								  IC[xd][yc],\
								  IC[xc][yu],\
								  IC[xc][yd],\
								  IC[xs][yu],\
								  IC[xs][yd],\
								  IC[xd][yu],\
								  IC[xd][yd])
	return (IC,CA) # swap IC <--> CA

def DrawCA(CA):
	for x,y in itertools.product(range(1,DIM[0]-1),range(1,DIM[1]-1)):												# the object surface of a dimension of RES x RES
		s.fill((0,0,(50+256*CA[x][y])%256))
		r.x,r.y = x*RES,y*RES										# get an object rectangle from the object surface and place it at position x,y
		screen.blit(s,r)															# link the object rectangle to the object surface
	pygame.display.flip()	# update the entire pygame display

def main():

	CA,IC = newMatrix(DIM[0]+1,DIM[1]+1,0),newMatrix(DIM[0]+1,DIM[1]+1,0)
	T = time.time()
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
					IC = SetIC(IC,event.pos[0],event.pos[1])	# aggiunge una perturbazione
		
		DrawCA(CA)
		CA,IC = UpdateCA(CA,IC)
		
		pygame.display.set_caption(f'CA Ripple Tank v.1 (c)2019 by Lumachina Software - @_°°           GEN:{NG}')
		NG +=1

	terminate(T,NG)

main()