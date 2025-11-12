#
# ca_ripple_tank_v0.py  ( simulated the ripple tank behaviour as seen at http://www.falstad.com/ripple/ )
#
# CopyRight 2019 by Lumachina Software @_°° Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)
#
#
# questa versione usa a = deepcopy(b) per copiare una matrice in un altra (non si comporta del tutto bene pero'...)


import time
import pygame, sys
from pygame.locals import *
import itertools
from copy import deepcopy
from matrici import newMatrix
from config_carippletank import *

pygame.init()
screen = pygame.display.set_mode((XRES,YRES))

global CA,NG
CA = newMatrix(DIM[0]+1,DIM[1]+1,0)
	
def terminate(t,ng):
	dt = time.time()-t
	print(f'Velocità :  {ng/dt} generazioni al secondo')			# stampa a console il numero di generazioni
	print(f'Terminato dopo {int(dt)} secondi')
	pygame.quit()
	sys.exit()	

def DrawCA():
	for x,y in itertools.product(range(1,DIM[0]-1),range(1,DIM[1]-1)):
		s = pygame.Surface((RES,RES))												# the object surface of a dimension of RES x RES
		s.fill((0,0,(50+200*CA[x][y])%256))
		r,r.x,r.y = s.get_rect(),x*RES,y*RES										# get an object rectangle from the object surface and place it at position x,y
		screen.blit(s,r)															# link the object rectangle to the object surface
	
	pygame.display.flip()	# update the entire pygame display

def SetCA(x,y):	CA[x//RES][y//RES] = Q

def GetNeighborhoods(i,j):
	# set the Moore's neighborhoods into a closed cylindrical world	
	xs = i-1	# sinistra
	xc = i		# centrale
	xd = i+1 	# destra
	yu = j+1	# alto
	yc = j		# centrale
	yd = j-1	# basso
	return xs,xc,xd,yu,yc,yd

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
		
def UpdateCA():
	# updating lattice using the Ripple Tank rule with Moore neighboroods
	IC = deepcopy(CA)
	for i,j in itertools.product(range(1,DIM[0]-1),range(1,DIM[1]-1)):
		xs,xc,xd,yu,yc,yd = GetNeighborhoods(i,j) # stabilisce quali sono i vicini della cellula
		CA[i][j] =  RippleTankRule(IC[xs][yc],\
								  CA[xc][yc],\
								  IC[xd][yc],\
								  IC[xc][yu],\
								  IC[xc][yd],\
								  IC[xs][yu],\
								  IC[xs][yd],\
								  IC[xd][yu],\
								  IC[xd][yd])	
	
def main():
		
	clock = pygame.time.Clock()

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
					SetCA(event.pos[0],event.pos[1])	# aggiunge una perturbazione
					
		DrawCA()
		
		NG += 1
		UpdateCA()
		pygame.display.set_caption(f'CA Ripple Tank (c)2019 by Lumachina Software - @_°°           GEN:{NG}')
		clock.tick(TICKS)
		
	terminate(t,NG)

main()
