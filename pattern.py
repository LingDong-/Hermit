
import pygame
import sys
import math
import utilities as u
import copy
import random
import noise

pygame.init()

class Dot():
	def __init__(self,x,y,a,r,adir=1,color = (180,180,180)):
		self.x = x
		self.y = y
		self.a = a
		self.adir = adir
		self.r = r
		self.s = 1
		self.color = color
		self.t = 0
		self.f = 0
	def crawl(self):
		self.x += self.s*math.cos(self.a)
		self.y -= self.s*math.sin(self.a)
		self.t += 1
		if self.t > self.r * 7:
			try:
				self.a += 0.0005*self.t**2*self.adir/self.r**3
			except:pass
		else:
			pass
			#self.a+=1*(noise.noise(self.t*0.01)-0.5)
			#self.r -= 1
	def draw(self,surf):
		#u.circle(surf,(245,245,245),[self.x,self.y+1],self.s/2)
		u.circle(surf,self.color,[self.x,self.y],self.s/2)

class Vine():
	def __init__(self,x,y,color = (180,180,180)):
		self.color =color
		self.dots = []
		self.dots.append(Dot(x,y,0,10,color = self.color))
		
	def grow(self,surf):
		
		for d in self.dots:
			d.crawl()
			d.draw(surf)
			if d.t == int(d.r * 7) and random.random() < 0.5 and d.r > 2:
				if len(self.dots) < 40:
					self.dots.append(Dot(d.x,d.y,0,d.r*(0.5+0.7*random.random()),-d.adir,self.color))
					
			if random.random() < 0.02 and d.r*50 > d.t > d.r * 6 and d.f < d.r/5 and d.r > 3:
				if len(self.dots) < 40:
					self.dots.append(Dot(d.x,d.y,0.5*(random.random()-0.5),d.r*(0.5+0.6*random.random()),-d.adir,self.color))
					d.f += 1
			
			
			if abs(d.t) > d.r*50:
				self.dots.remove(d)
				if len(self.dots) < 1:
					self.dots.append(Dot(d.x,d.y,0.5*(random.random()-0.5),d.r*(0.5+0.6*random.random()),-d.adir,self.color))
		
					

		
if __name__ == "__main__":
	screen = pygame.display.set_mode([640,320])
	screen.fill([240,240,240])
	vine = Vine(0,160)
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		u.text(screen,20,160+5,"Loading... ",(180,180,180))
		#screen.fill([240,240,240])	
		vine.grow(screen)
		pygame.display.flip()
