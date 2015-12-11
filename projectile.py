import pygame
import sys
import math
import utilities as u
import copy
import random
import noise

pygame.init()

class Arrow():
	def __init__(self,x,y):
		self.color = (150,150,150)
		self.x=x
		self.y=y
		self.l=20
		self.a=0
		self.spd=10
		self.v=[self.spd,0]
		self.g=0.2
		#self.body = None
		#self.state = 0
		
		self.flicker = 1
	def calcA(self):
		return math.degrees(math.atan2(self.v[1],self.v[0]))
		
	def calcV(self):
		return [self.spd*math.cos(math.radians(self.a)), -self.spd*math.sin(math.radians(self.a))]
		
		
	def calcHead(self):
		return self.x+self.l*math.cos(math.radians(self.a)), self.y+self.l*math.sin(math.radians(self.a))

	def calcFeather(self):
		return self.x+self.l*0.3*math.cos(math.radians(self.a)), self.y+self.l*0.3*math.sin(math.radians(self.a))
		
		
	def draw(self,surf):
		u.line(surf,[245,245,245],[self.x,self.y],self.calcFeather(),3)
		u.line(surf,self.color,[self.x,self.y],self.calcHead(),random.randrange(0,2)*self.flicker+1)
		
		
	def fly(self):
		self.a=self.calcA()
		
		self.x += self.v[0]
		self.y += self.v[1]
		self.v[1]+=self.g
		
		
