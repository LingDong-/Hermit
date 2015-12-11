import pygame
import sys
import math
import random
import utilities as u


def drawTree(**p):
	if p['depth'] < p['maxdepth']:
		
		if p['height'] <1:return
		
		dep = p['depth']
		p['width'] *= p['dwidth'](dep)		
		
		
		x0 = p['x']+math.cos(p['angle'])*p['trunk']
		y0 = p['y']-math.sin(p['angle'])*p['trunk']
		u.line(p['surf'],p['color'],[p['x'],p['y']],[x0,y0],p['width'])
		
		
		p['width'] *= p['dwidth'](dep)
		a1 = p['angle']-p['opening']*p['dopening'](dep)
		a2 = p['angle']+p['opening']*p['dopening'](dep)
		
		h1 = p['height'] * p['dheight'](dep)
		x1 = x0+math.cos(a1)*h1
		y1 = y0-math.sin(a1)*h1

		h2 = p['height'] * p['dheight'](dep)
		x2 = x0+math.cos(a2)*h2
		y2 = y0-math.sin(a2)*h2
		
		#u.text(p['surf'],x1,y1,str(dep),(0,150,0))
		#u.text(p['surf'],x2,y2,str(dep),(0,150,0))			
		
		u.line(p['surf'],p['color'],[x0,y0],[x1,y1],p['width'])
		u.line(p['surf'],p['color'],[x0,y0],[x2,y2],p['width'])
		
	
		p['trunk'] *= p['dtrunk'](dep)
		
		p['depth'] += .5
		p['x'],p['y'],p['height'],p['angle'] = x1,y1,h1,a1-p['dangle'](dep)
		
		drawTree(**p)
		
		
		p['depth'] += .5
		p['x'],p['y'],p['height'],p['angle'] = x2,y2,h2,a2+p['dangle'](dep)
		drawTree(**p)
	else:
		return
	

def tree1(surf,x,y,shade=0):
	drawTree(surf = surf,
			 x = x,
			 y = y,
			 angle = math.pi/2,
			 dangle = lambda dep: -(random.random()-0.5)*math.pi/3,
			 
			 trunk = 50,
			 dtrunk = lambda dep: 0.8*random.random(),				 				 
			 
			 width = 8,
			 dwidth = lambda dep: random.random()*0.2+0.8,
			 
			 height = 50,
			 dheight = lambda dep: random.random()*0.6+0.4,
			 
			 opening = math.pi/6,
			 dopening = lambda dep: 0.8 + random.random()*0.5,
			 
			 color = (100+shade,100+shade,100+shade),
			 depth = 0,
			 maxdepth = 10
			)
			
def tree2(surf,x,y,shade=0):
	drawTree(surf = surf,
			 x = x,
			 y = y,
			 angle = math.pi/2,
			 dangle = lambda dep: 0,
			 
			 trunk = 20,
			 dtrunk = lambda dep: 0.9,			 				 
			 
			 width = 10,
			 dwidth = lambda dep: random.random()*0.3+0.7,
			 
			 height = 100,
			 dheight = lambda dep: random.random()*0.6+0.3,
			 
			 opening = math.pi/3,
			 dopening = lambda dep: ((dep*2)%2)*(0.8+random.random()*0.4),#*(dep<2),
			 
			 color = (100+shade,100+shade,100+shade),
			 depth = 0,
			 maxdepth = 12
			)

def tree3(surf,x,y,shade=0):
	drawTree(surf = surf,
			 x = x,
			 y = y,
			 angle = math.pi/2,
			 dangle = lambda dep: -(random.random()-0.5)*math.pi/3,
			 
			 trunk = 0,
			 dtrunk = lambda dep: 0.8*random.random(),				 				 
			 
			 width = 6,
			 dwidth = lambda dep: random.random()*0.2+0.8,
			 
			 height = 100,
			 dheight = lambda dep: random.random()*0.7+0.2,
			 
			 opening = math.pi/3,
			 dopening = lambda dep: random.random()*2-1,
			 
			 color = (100+shade,100+shade,100+shade),
			 depth = 0,
			 maxdepth = 10
			)



def tree4(surf,x,y,shade=0):
	drawTree(surf = surf,
			 x = x,
			 y = y,
			 angle = math.pi/2,
			 dangle = lambda dep: (-math.pi/6)+((random.random()-0.5)*(dep))*2,
			 
			 trunk = 50,
			 dtrunk = lambda dep: 0.8*random.random(),				 				 
			 
			 width = 8,
			 dwidth = lambda dep: random.random()*0.2+0.8,
			 
			 height = 50,
			 dheight = lambda dep: random.random()*0.5+0.5,
			 
			 opening = math.pi/5,
			 dopening = lambda dep: 0.8 + random.random()*0.5*dep*2,
			 
			 color = (100+shade,100+shade,100+shade),
			 depth = 0,
			 maxdepth = 10
			)

if __name__ == "__main__":
	screen = pygame.display.set_mode([800,500])
	screen.fill([240,240,240])
	for i in range(0,4):
		[tree1,tree2,tree3,tree4][i](screen,100+i*200,500,30)

	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_SPACE:
					print event.key==pygame.K_SPACE
					screen.fill([240,240,240])
					for i in range(0,4):
						[tree1,tree2,tree3,tree4][i](screen,100+i*200,500,30)
		pygame.display.flip()
