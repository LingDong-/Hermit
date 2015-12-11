

import pygame
import sys
import math
import utilities as u
import copy
import random
import noise
import numpy as np

pygame.init()

class GFont():
	font = {
	' ' : [],
	'H' : [['l',0,0,0,4],['l',1.8,0,1.8,4],['l',0,2,1.8,2]],

	
	'a' : [['a',0,2,2,0,360], ['l',2,3,2,4]],
	'b' : [['a',0,2,2,0,360], ['l',0,0,0,3]],
	'c' : [['a',0,2,2,30,330]],
	'd' : [['a',0,2,2,0,360], ['l',2,0,2,4]],
	'e' : [['a',0,2,2,0,340], ['l',0,3,2,3]],
	'f' : [['a',0,0,2,30,180],['l',0,1,0,5], ['l',0,2,2,2]],
	'g' : [['a',0,2,2,0,360], ['l',2,3,2,5], ['a',0,4,2,180,360]],
	'h' : [['a',0,2,2,0,180], ['l',0,0,0,4], ['l',2,3,2,4]],
	'i' : [['l',1,0,1,0.5],  ['l',1,2,1,4]],
	'j' : [['l',1,0,1,0.5],  ['l',1,2,1,5], ['a',-1,4,2,180,360]],
	'k' : [['l',0,0,0,4],    ['l',2,2,0,3], ['l',0,3,2,4]],
	'l' : [['l',0,0,0,3],    ['a',0,2,2,180,360]],
	'm' : [['a',0,2,2,0,90],  ['l',0,2,0,4], ['l',2,3,2,4], ['l',1,2,1,4],['l',0,2,1,2]],
	'n' : [['a',0,2,2,0,180], ['l',0,2,0,4], ['l',2,3,2,4]],
	'o' : [['a',0,2,2,0,360]],
	'p' : [['a',0,2,2,0,360], ['l',0,3,0,6]],
	'q' : [['a',0,2,2,0,360], ['l',2,2,2,6]],
	'r' : [['a',.5,2,2,90,180],['l',.5,2,.5,4]],
	's' : [['a',0,2,2,0,180], ['a',0,3,2,180,360],['l',0,3,2,4]],
	't' : [['l',0,0,0,3],    ['a',0,2,2,180,360],['l',0,2,2,2]],
	'u' : [['l',2,2,2,4],    ['a',0,2,2,180,360],['l',0,2,0,3]],
	'v' : [['l',0,2,1,4],    ['l',2,2,1,4]],
	'w' : [['l',0,2,0,4],    ['a',0,2,2,270,360],['l',2,2,2,3], ['l',1,2,1,4],['l',0,4,1,4]],
	'x' : [['l',0,2,2,4],    ['l',0,4,2,2]],
	'y' : [['l',2,2,2,5],    ['a',0,2,2,180,360],['l',0,2,0,3],['a',0,4,2,180,360]],
	'z' : [['l',0,2,2,2],    ['l',2,2,0,4],['l',0,4,2,4]]
	}
	def __init__(self,size,width,color=(0,0,0)):
		self.s = size
		self.w = width
		self.color = color
	def drawStr(self,surf,st,x,y,size=1):
		s = self
		for i in range(0,len(st)):
			sp = i*2.3
			for f in self.font[st[i]]:
				if f[0] == 'a':
					pygame.draw.arc(surf,s.color,  [f[1]*s.s*size+x+sp*s.s*size, f[2]*s.s*size+y, f[3]*s.s*size, f[3]*s.s*size],math.radians(f[4]),math.radians(f[5]),s.w)
				if f[0] == 'l':
					pygame.draw.line(surf,s.color, [f[1]*s.s*size+x+sp*s.s*size, f[2]*s.s*size+y],[f[3]*s.s*size+x+sp*s.s*size,f[4]*s.s*size+y],s.w)
			
		
		



		
if __name__ == "__main__":
	screen = pygame.display.set_mode([640,320])
	gfont = GFont(20,2)
	while 1:

		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
	
		screen.fill([255,255,255])
		gfont.drawStr(screen,"by lingdong",10,100)
		
		
		pygame.display.flip()
		
