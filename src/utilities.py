import pygame
import math

pygame.init()
sysf = pygame.font.SysFont(pygame.font.get_default_font(),16)

def lmap(f,l):
		""" given a function and a list
			maping the function on the list
			return the mapped list
		"""
	return list(map(f,l))

def toInt(n):
		""" transform a number to integer
		"""
	return int(n)

def line(surface,color,start_pos,end_pos,width=1):
		""" vectorized line drawing function
			map all parameters into ints since pygame accepts only integer coordinates
		"""
	return pygame.draw.line(surface,color,lmap(toInt,start_pos),lmap(toInt,end_pos),int(math.ceil(width)))
	
def polygon(surface,color,pointlist,width=0):
		""" draw a polygon using pointlist
		"""
	return pygame.draw.polygon(surface,color,lmap(lambda l: lmap(toInt, l),pointlist),int(round(width)))
		
def circle(surface,color,pos,radius,width=0):
		""" draw a circle
		"""
	return pygame.draw.circle(surface,color,lmap(toInt,pos),int(radius),int(round(width)))
		
	
def text(surf,x,y,t,color=(0,0,0),Font=sysf):
		""" render text
		"""
	fs = Font.render(t,False,color)
	surf.blit(fs,[x,y])

def triwave(t,a=2*math.pi):
		""" generate a triangle wave
		"""
	t = float(t)
	a = float(a)
	return (2/a)*(t-a*int(t/a+0.5))*(-1)**int(t/a+0.5)

def trapwave(x):
		""" generate a trapezoidal wave
		"""
	return ((8*math.sqrt(2))/(math.pi*math.pi)) * (math.sin(x)+math.sin(3*x)/9.0)

def dist(x1,y1,x2,y2):
		""" return the distance between two points
		"""
	return math.sqrt((x1-x2)**2+(y1-y2)**2)
