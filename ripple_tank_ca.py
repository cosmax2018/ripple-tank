#
# ca_ripple_tank_v2.py with PyGame, Numpy and Numba ! 
#
# simulated the ripple tank behaviour as seen at http://www.falstad.com/ripple/ 
#
# CopyRight 2019-2022 by Lumachina Software @_°° Massimiliano Cosmelli (massimiliano.cosmelli@gmail.com)
# 
#

import time
import numpy as np
import pygame, sys
from pygame.locals import *

from numba import jit

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

def SetIC(IC,x,y):
	IC[x//RES][y//RES] = INTENSITY*Q
	return IC
	
@jit(nopython=True,nogil=True)
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
			
@jit(nopython=True,nogil=True)
def UpdateCA(CA,IC):
	# updating lattice using the Ripple Tank rule with Moore neighboroods
	for i in range(1,DIM[0]-1):
		for j in range(1,DIM[1]-1):
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

# def DrawCA(CA,rr,gg,bb):
	# ''' versione piu' veloce !'''
	# for x in range(1,DIM[0]-1):
		# for y in range(1,DIM[1]-1):				# the object surface of a dimension of RES x RES
			# s.fill((0,0,255*CA[x][y]%256))
			# r.x,r.y = x*RES,y*RES				# get an object rectangle from the object surface and place it at position x,y
			# screen.blit(s,r)					# link the object rectangle to the object surface
	# pygame.display.flip()						# update the entire pygame display

def DrawCA(c,rr,gg,bb):
	''' versione piu' lenta ma con i colori RGB '''
	for x in range(1,DIM[0]-1):
		for y in range(1,DIM[1]-1):							
			s.fill((rr*c[x][y]%256,gg*c[x][y]%256,bb*c[x][y]%256))
			r.x,r.y = x*RES,y*RES	# get an object rectangle from the object surface and place it at position x,y
			screen.blit(s,r)		# link the object rectangle to the object surface
	pygame.display.flip()			# update the entire pygame display
	
def main(a):

	# eg.:    py ca_ripple_tank_v2.py 0 0 255
	try:
		RED,GREEN,BLUE = int(a[0]),int(a[1]),int(a[2])
	except:
		RED,GREEN,BLUE = 250,250,250		# rgb components
	finally:
		print(f'Ripple Tank RGB Colors Parameters RED,GREEN,BLUE:{RED},{GREEN},{BLUE}')
	
	CA,IC = np.zeros((DIM[0]+1,DIM[1]+1)),np.zeros((DIM[0]+1,DIM[1]+1))
	
	NG,T = 0,time.time()

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
					
		DrawCA(CA,RED,GREEN,BLUE)
		CA,IC = UpdateCA(CA,IC)
		
		pygame.display.set_caption(f'CA Ripple Tank v.2 (c)2022 by Lumachina Software - @_°°           GEN:{NG}')
		NG +=1
		
	terminate(T,NG)

main(sys.argv[1:])
