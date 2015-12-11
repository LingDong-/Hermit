import pygame
import sys
import math
import utilities as u
import copy
import random
import noise

pygame.init()

class Particle():
	def __init__(self,x,y,v):
		self.x = x
		self.y = y
		self.v = v
		self.g = 0.2
		
		self.color = (100,100,100)
		self.s = 1
		self.life = 50
		
	def fly(self):
		self.x += self.v[0]
		self.y += self.v[1]
		self.v[1] += self.g
		self.life -= 1
	def draw(self,surf):
		u.circle(surf,self.color,[self.x,self.y],self.s/2)
		
class ParticleCtrl():
	def __init__(self):
		self.particles = []
	def emit(self):
		for p in self.particles:
			p.fly()
			if p.life <= 0:
				self.particles.remove(p)
		
	def draw(self,surf):
		for p in self.particles:
			p.draw(surf)
