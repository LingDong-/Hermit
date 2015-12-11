import pygame
import sys
import math
import utilities as u
import copy
import random
import noise
import projectile
import tree
import settings

pygame.init()

class Animal(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.yo = 0
		self.s = 2
		self.t = 0
		self.aspd = 0.05
		self.skel = []
		self.color = (150,150,150)
		self.animations = [[]]
		self.dir = 1
		self.spd = 0.5
		self.timers = []
		self.health = 100
		
	def __str__(self):
		return self.skel
		
	def super(self):
		return super(type(self),self)
		
	def calcCoord(self,n):
		if n == self.skel[n][2]:
			return [0,0,0]
		else:
			trl = self.skel[n]
			pc = self.calcCoord(trl[2])
			tc = [0,0,0]
			
			tc[0] = pc[0] + trl[1]*math.cos(math.radians(trl[0]+pc[2]))
			tc[1] = pc[1] - trl[1]*math.sin(math.radians(trl[0]+pc[2]))
			tc[2] = pc[2] + trl[0]
			return tc
	def to(self,r,l,n,spd=3):
		self.skel[r][l] += (n-self.skel[r][l])/float(spd)
		
	def animate(self):
		for a in self.animations[0]:
			if a[0][0] == "trans":
				if a[0][1] == "x":
					self.x+=(a[1][0]-self.x)/float(a[1][1])
					#self.dir = (a[1][0]-self.x>0)*2-1
					self.walk()
				if a[0][1] == "xt":
					self.x+=(a[1][0]-self.x)/float(a[1][1])

				elif a[0][1] == "y":
					self.y+=(a[1][0]-self.y)/float(a[1][1])
			else:
				self.skel[a[0][0]][a[0][1]]+=(a[1][0]-self.skel[a[0][0]][a[0][1]])/float(a[1][1])
			a[1][1]-=1
			if a[1][1]<=0:
				a.remove(a[1])
			if len(a) <= 1:
				self.animations[0].remove(a)
			if len(self.animations[0]) == 0:
				self.animations.pop(0)
			if len(self.animations)==0:
				self.animations.append([])
		
		for ti in self.timers:
			ti[0] -= 1
			if ti[0] == 0:
				ti[1](*ti[2])
				self.timers.remove(ti)
		
		
				
	def addanim(self,skn,rol,dest,t):
		na = [[skn,rol],[dest,t]]
		for a in self.animations[-1]:
			if a[0][0]==na[0][0] and a[0][1]==na[0][1]:
				a.append(na[1])
				return
		self.animations[-1].append(na)
		
	def animback(self,t,exceptions=[]):
		for i in range(0,len(self.skel)):
			if i not in exceptions:
				self.addanim(i,0,self.ssk[i][0],t)
				self.addanim(i,1,self.ssk[i][1],t)

		
	
		
	def poly(self,surf,*args):
		u.polygon(surf,self.color,u.lmap(lambda l: [self.x+l[0]*self.s*self.dir,self.y+self.yo+l[1]*self.s], args))
	def circle(self,surf,pos,radius):
		u.circle(surf,self.color,[self.x+pos[0]*self.s*self.dir,self.y+self.yo+pos[1]*self.s],radius*self.s)
	def line(self,surf,start_pos,end_pos,width=1):
		u.line  (surf,self.color,[self.x+start_pos[0]*self.s*self.dir,self.y+self.yo+start_pos[1]*self.s],
								 [self.x+  end_pos[0]*self.s*self.dir,self.y+self.yo+  end_pos[1]*self.s],width*self.s)
		
	
	def drawSkel(self,surf):
		for i in range(0,len(self.skel)):
			c = self.calcCoord(i)
			pc = self.calcCoord(self.skel[i][2])
			self.line(surf,[c[0],c[1]],[pc[0],pc[1]],1)
				


class Horse(Animal):
	def __init__(self,x,y):
		
		super(Horse,self).__init__(x,y)
		self.phase = "playing"
		self.skel=[ [-90,10, 1],		
					[ 30,20, 2],#1
					[  0, 0, 2],
					[190,10, 2],
					[-20,10, 3],
					[ 50,10, 4],#5
					[ 30,15, 5],
					[-70,10, 2],
					[-10,12, 7],
					[  0,12, 8],
					[-30,12, 7],#10
					[ 20,12,10],
					[ 70,10, 4],
					[ 70,10,12],
					[-90,10,13],
					[ 45,12,14],#15
					[ 85,10,12],
					[-90,10,16],
					[ 45,12,17],#18
				]
		self.ssk = copy.deepcopy(self.skel)

	def draw(self,surf):
		cd = []
		for i in range(len(self.skel)):
			cd.append(self.calcCoord(i)[:2])
			
		self.poly(surf, cd[2],
						[cd[7][0]+2,cd[7][1]+2],  [cd[3][0]+5,cd[3][1]+13],
						cd[12],   cd[4],   [cd[4][0]+4,cd[4][1]],   cd[3]
						)
		self.poly(surf, cd[2],   [cd[1][0]-3,cd[1][1]],
						[cd[1][0]+1,cd[1][1]-1],   [cd[1][0]+3,cd[1][1]],
						[cd[1][0]+2,cd[1][1]+1],   [cd[0][0]+1,cd[0][1]-1],
						[cd[0][0]-1,cd[0][1]+1],   [cd[1][0]-1,cd[1][1]+5],
						[(cd[2][0]+cd[1][0])/2,(cd[2][1]+cd[1][1])/2+8],
						[cd[7][0]+2,cd[7][1]+2],
						)			
		self.poly(surf, cd[2],  [cd[7][0]+2,cd[7][1]],  [cd[8][0]+2,cd[8][1]],
						[cd[9][0]+2,cd[9][1]],   [cd[9][0],cd[9][1]],
						cd[8],   [cd[7][0]-6,cd[7][1]]
						)		
		self.poly(surf, cd[2],  [cd[7][0]+2,cd[7][1]],  [cd[10][0]+2,cd[10][1]],
						[cd[11][0]+2,cd[11][1]],   [cd[11][0],cd[11][1]],
						cd[10],   [cd[7][0]-6,cd[7][1]]
						)	
		self.poly(surf, cd[3],cd[2],cd[13],cd[12],cd[4])	
		self.poly(surf, cd[3],cd[2],cd[16],cd[12],cd[4])
		
		self.poly(surf, cd[12],cd[13],
						[cd[14][0]+2,cd[14][1]],   [cd[15][0]+1,cd[15][1]],
						[cd[15][0]-1,cd[15][1]],   [cd[14][0],cd[14][1]],
						[(cd[12][0]+cd[14][0])/2+2,(cd[12][1]+cd[14][1])/2]
						)
		self.poly(surf, cd[12],cd[16],
						[cd[17][0]+2,cd[17][1]],   [cd[18][0]+1,cd[18][1]],
						[cd[18][0]-1,cd[18][1]],   [cd[17][0],cd[17][1]],
						[(cd[12][0]+cd[17][0])/2+2,(cd[12][1]+cd[17][1])/2]
						)
						
		self.poly(surf, [cd[4][0],cd[4][1]],cd[5],cd[6])
						


	def walk(self):
		s = self
		s.t += 1
		
		s.to(1,0,30-math.cos(s.t*s.aspd*2)*5)
		s.to(0,0,-85+math.cos(s.t*s.aspd*2)*10)
		
		s.to(3,0,190+math.cos(s.t*s.aspd*2)*1)
		s.to(4,0,-20+math.cos(s.t*s.aspd*2)*2)
		
		s.to(6,0,30+math.cos(s.t*s.aspd*1.5)*10)
		
		s.to(7,1,9-math.cos(s.t*s.aspd*2)*1)
		
		s.to(8,0,-18+math.sin(s.t*s.aspd)*25)
		s.to(9,0,-20-math.cos(s.t*s.aspd)*20)
		
		s.to(10,0,-18+math.sin(s.t*s.aspd+math.pi)*25)
		s.to(11,0,-20-math.cos(s.t*s.aspd+math.pi)*20)
		
		s.to(12,1,7+math.cos(s.t*s.aspd*2)*1)
		
		s.to(13,0,75+math.cos(s.t*s.aspd)*15)
		s.to(14,0,-90+math.cos(s.t*s.aspd)*15)
		s.to(15,0,55+math.sin(s.t*s.aspd)*2)

		s.to(16,0,75+math.cos(s.t*s.aspd+math.pi)*15)
		s.to(17,0,-90+math.cos(s.t*s.aspd+math.pi)*20)
		s.to(18,0,55+math.sin(s.t*s.aspd+math.pi)*2)	

	def rest(self):
		s = self
		s.t +=1
		for i in range(0,len(s.skel)):
			if i != 6 and i != 1:
				s.to(i,0,s.ssk[i][0]+noise.noise(i*0.05,s.t*0.05),5)
		s.to(6,0,30+math.cos(s.t*s.aspd*0.5)*10)
		
		noi = max(min((noise.noise(s.t*s.aspd*0.05)-0.4)*40,1),-1)
		s.to(1,0,-5+noi*50,5)
		s.to(0,0,-40-noi*40,5)
		
		#s.to(1,1,25+math.cos(s.t*s.aspd*0.5+math.pi)*2)
class Unicorn(Horse):
	def __init__(self,x,y):
		super(Unicorn,self).__init__(x,y)
	def draw(self,surf):
		super(Unicorn,self).draw(surf)
		
		cd = []
		for i in range(len(self.skel)):
			cd.append(self.calcCoord(i)[:2])
		self.poly(surf,cd[1],[cd[1][0]+(cd[0][0]-cd[1][0])/3.0,cd[1][1]+(cd[0][1]-cd[1][1])/3.0],
			[cd[1][0]+20*math.cos(math.radians(-self.calcCoord(1)[2]+5*self.dir)),cd[1][1]+50*math.sin(math.radians(-self.calcCoord(1)[2]+5*self.dir))])
		self.color = [random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)]

class Deer(Horse):
	def __init__(self,x,y,color=(140,140,140),s=1.1):
		super(Deer,self).__init__(x,y)
		self.skel[1][1] = 15
		self.skel[5][1] = 5
		self.skel[6][1] = 5
		self.ssk = copy.deepcopy(self.skel)
		self.s = s
		self.dir = -1
		self.horn = pygame.Surface([100*self.s,50*self.s])
		self.horn.fill([255,0,255])
		self.horn.set_colorkey([255,0,255])
		self.color = color
		
		self.spd = 0.6
		self.tx = 0
		
		tree.drawTree(surf = self.horn,
				 x = 50*self.s,#cd[1][0]*self.s+self.x,
				 y = 50*self.s,#cd[1][1]*self.s+self.y+self.yo,
				 angle = math.pi*2/3,
				 dangle = lambda dep: 0,#-(random.random()-0.5)*math.pi/3,
				 
				 trunk = 0,
				 dtrunk = lambda dep: 0,#0.8*random.random(),				 				 
				 
				 width = 3*self.s*0.6,
				 dwidth = lambda dep: random.random()*0.1+0.9,
				 
				 height = 4*self.s*0.6,
				 dheight = lambda dep: 1.2*((dep*2)%2)+0.4,#(((dep+1)*2)%2),
				 
				 opening = math.pi/6,
				 dopening = lambda dep: 0.5+random.random()*0.5,
				 
				 color = self.color,
				 depth = 0,
				 maxdepth = 6
				)	
		if self.dir == -1:
			self.horn = pygame.transform.flip(self.horn,1,0)
		#pygame.draw.rect(self.horn,(255,0,0),[0,0,self.horn.get_width()/2,self.horn.get_height()],5)
		self.shorn = self.horn	
		#self.horn.get_rect().center=(50*self.s,50*self.s)
		#self.horn = pygame.transform.rotate(self.horn, 90)	
		#self.horn.get_rect().center=(50*self.s,50*self.s)
		#print self.horn.get_rect().center
		#self.horn = pygame.transform.scale(self.horn, (50*self.s,35*self.s))
	def draw(self,surf):
		super(Deer,self).draw(surf)
		cd = []
		for i in range(len(self.skel)):
			cd.append(self.calcCoord(i)[:2])
		#print self.horn.get_width()
		self.horn = self.shorn
		#self.tx = (self.tx+0.5)%90.0
		#a = self.tx
		a = self.dir*(self.calcCoord(0)[2]+30)

		self.horn = pygame.transform.rotate(self.horn, a)	
		#cd[1] = [-80,-80]
		if self.dir == 1:
			hc = [cd[1][0]*self.s+self.x     - 50*self.s*math.cos(math.radians(90+a))-70*self.s*math.cos(math.radians(45-a)),
								 cd[1][1]*self.s+self.y+self.yo        - 68*self.s*math.sin(math.radians(45-a))]
		else:
			#hc = [-cd[1][0]*self.s+self.x   - 50*self.s*math.sin(math.radians(a)),
			#					 cd[1][1]*self.s+self.y+self.yo    - 50*self.s*math.sin(math.radians(a)) - 50*self.s*math.cos(math.radians(a))]			
			hc = [-cd[1][0]*self.s+self.x   - 50*self.s*math.cos(math.radians(a))-49*self.s*math.sin(math.radians(a)),
								 cd[1][1]*self.s+self.y+self.yo  - 50*self.s*math.sin(math.radians(a)) - 49*self.s*math.cos(math.radians(a))]


		#pygame.draw.rect(surf,(0,255,0),[hc[0],hc[1],self.horn.get_width()/2,self.horn.get_height()],1)
		
		surf.blit(self.horn,[hc[0],hc[1]])
		




class Man(Animal):
	def __init__(self,x,y):
		super(Man,self).__init__(x,y)
		self.skel=[ [ -20, 5, 1],		
					[ 105,20, 2],#1
					[   0, 0, 2],
					[-100,30, 2],
					[-170, 8, 1],
					[  50, 5, 4],#5
					[-160, 8, 1],
					[  20, 5, 6],
					[ 180, 0, 7],
					[-180, 0, 7],
					[   0, 0, 5] #10
				  ]
		self.ssk = copy.deepcopy(self.skel)
		self.f1 = 6
		self.f2 = 6
		self.s1 = 0
		self.s2 = 0
		self.status = ["",""]
		self.assets = []
		self.eventdelay = 0
		self.arrows = []
		
		
		
	def draw(self,surf):
		cd = []
		for i in range(len(self.skel)):
			cd.append(self.calcCoord(i)[:2])		
		s = self
		s.poly(surf, [(cd[0][0]+cd[1][0])/2,(cd[0][1]+cd[1][1])/2],
					 [cd[1][0]+3,cd[1][1]+3],   [cd[2][0]+3,cd[2][1]],
					 [cd[2][0]-4,cd[2][1]],   [cd[1][0]-2,cd[1][1]+5]
					 )
					 
		s.poly(surf, [cd[2][0]-4,cd[2][1]],
					 [(cd[2][0]+cd[3][0])/2-s.f1/2,(cd[2][1]+cd[3][1])/2],
					 [cd[3][0]-s.f1,cd[3][1]],   [cd[3][0]+s.f2,cd[3][1]],
					 [cd[2][0]+3,cd[2][1]]
					 )
					 

		s.poly(surf, [cd[1][0],cd[1][1]],   [cd[4][0],cd[4][1]],
					 [cd[4][0]+s.s1,cd[4][1]+15],   [cd[1][0]-2,cd[1][1]+5]
					 )			 
		s.poly(surf, [cd[4][0],cd[4][1]],
					 [cd[5][0],cd[5][1]],   [cd[5][0]+s.s1,cd[5][1]+12],
					 [cd[4][0]+s.s1,cd[4][1]+15]
					 )
					 					 
		s.poly(surf, [cd[1][0],cd[1][1]],   [cd[6][0],cd[6][1]],
					 [cd[7][0],cd[7][1]],   [cd[7][0]+s.s2,cd[7][1]+12],
					 [cd[6][0]+s.s2,cd[6][1]+15],   [cd[1][0]-2,cd[1][1]+5]
					 )
		#s.circle(surf,[cd[0][0],cd[0][1]],1.5)
		s.line(surf,cd[0],cd[1],3)	
		if "bow" in self.assets:
			s.line(surf,cd[7],cd[8],2)
			s.line(surf,cd[7],cd[9],2)
			
		if "arrow" in self.assets:
			s.line(surf,cd[5],cd[10],1)

		if "cup" in self.assets:
			s.line(surf,cd[5],cd[10],2)

	def walk(self):
		s = self
		s.t += 1
		s.f1 = 6 + math.cos(s.t*s.aspd*2)*2 +noise.noise(s.t*s.aspd)*2
		s.f2 = 8 + math.cos(s.t*s.aspd*2)*2
		#print self.animations
		if self.status[1] == "":
			for i in range(0,len(s.skel)):
				for j in range(0,max(0,len(self.animations))):
					for a in self.animations[j]:
						if i == a[0][0]:
						#print "y"
							return
				s.to(i,0,s.ssk[i][0]+10*(noise.noise(i*0.05,s.t*0.05)-0.5),2)
	def rest(self):
		s = self
		s.t+=1
		noi = noise.noise(s.t*s.aspd*0.5)
		s.f1 += (6+(noi*5)-s.f1)/2
		s.s1 += (1-(noi*4)-s.s1)/2
		s.s2 += (1-(noi*4)-s.s2)/2
		

	def mount(self,horse):

		self.addanim("trans","y",self.y,50)
		horse.addanim("trans","x",self.x+horse.dir*horse.s*7,50)
		self.animations.append([])
		self.addanim(1,0,60,30)
		self.addanim("trans","y",horse.y+horse.s*0.5+(horse.yo-self.yo),20)
		self.animations.append([])
		self.addanim("trans","y",horse.y-horse.s*2+(horse.yo-self.yo),20)
		self.addanim(1,0,100,20)
		self.addanim(3,0,-120,20)
		self.addanim(3,0,-80,10)
		self.addanim(3,1,30,30)
		self.addanim(3,1,10,20)
		self.status[0] = "mounting"
		def f(x): self.status[0]='mounted'
		self.timers.append([120,f,[0]])
		
	def dismount(self,horse):
		self.addanim(3,0,-120,20)
		self.addanim(3,0,-80,20)
		self.addanim(3,0,-100,10)
		self.addanim(3,1,30,30)
		self.addanim(1,0,60,20)
		self.addanim("trans","y",0,60)
		self.addanim(1,0,105,40)
		#self.animations.append([])
		#self.addanim("trans","x",horse.x+horse.s*50,100)
		horse.addanim("trans","y",horse.y,60)
		horse.animations.append([])
		horse.addanim("trans","x",self.x-horse.s*50,50)
		self.status[0] = "dismounting"
		def f(x): self.status[0]=''
		self.timers.append([80,f,[0]])	
	
	def drawbow(self):

		if "prepares" in self.status[1]:
			self.status[1]="bow starts drawing"
			self.assets.append("bow")
			self.assets.append("arrow")
			self.animations = [[]]
			self.addanim(1,0,80,20)
			
			self.addanim(8,1,20,25)
			self.addanim(9,1,20,25)
			
			self.addanim(8,0,90,1)
			self.addanim(9,0,-90,1)
			self.addanim(10,1,25,10)
			self.addanim(10,0,-15,10)
			def f(x):
				self.status[1]="bow is drawing"
			self.timers.append([25,f,[0],"drawbow"])
		elif self.status[1] == "bow is drawing":
			self.to(1,0,110,15)
			self.to(4,0,70,15)
			self.to(5,0,-160,15)
			self.to(6,0,-100,15)
			self.to(7,0,0,15)
			
			self.to(8,0,100,15)
			self.to(9,0,-100,15)
			
			
			if abs(self.skel[1][0]-110)<1:
				self.status[1]="bow is tightening"
		elif self.status[1] == "bow is tightening":
			self.to(4,1,10,50)
			self.to(8,0,110,50)
			self.to(9,0,-110,50)	
			self.to(1,0,120,50)
		
		
						
	def releasebow(self):
		self.status[1] = "bow is releasing"
		self.addanim(8,0,90,3)
		self.addanim(9,0,-90,3)
		self.addanim(8,0,92,5)
		self.addanim(9,0,-92,5)
		self.addanim(5,0,-130,5)
		if "arrow" in self.assets:
			self.assets.remove("arrow")
			arr = projectile.Arrow(self.x+self.calcCoord(5)[0]*self.s*self.dir,self.yo+self.y+self.calcCoord(5)[1]*self.s)
			arr.a = self.calcCoord(10)[2]
			#print(arr.a)
			arr.l = 25*self.s
			arr.spd = 1+0.05*max(1,self.skel[1][0]-100)*max(1,self.skel[8][0]-90)
			arr.v = arr.calcV()
			arr.color = self.color
			self.arrows.append(arr)
			
		def f(x):
			self.addanim(8,1,0,20)
			self.addanim(9,1,0,20)
			self.animback(20,exceptions=[3,8,9])
			self.status[1] = ""
			def g(x):
				self.assets.remove("bow")
				self.timers.append([25,g,[0],"removebow"])
		self.timers.append([25,f,[0],"releasebow"])


	def drink(self):
		self.addanim(4,0,-140,20)
		self.addanim(5,0,60,20)

		self.addanim(0,0,-20,20)
		self.addanim(10,1,3,20)
		self.addanim(10,0,80,20)
		
		self.animations.append([])
		
		self.addanim(4,0,-90,20)
		self.addanim(5,0,0,20)
		self.addanim(0,0,0,20)
		
		self.animations.append([])
		self.addanim(4,0,-110,20)
		self.addanim(5,0,30,20)

		self.animations.append([])		
		
		self.addanim(4,0,-60,30)
		self.addanim(5,0,120,30)
		self.addanim(1,0,120,30)
		self.addanim(0,0,40,30)
		self.addanim(10,0,45,30)
		
		self.animations.append([])
		self.addanim(10,0,50,30)
		self.addanim(0,0,50,30)
		
		self.animations.append([])		
		self.animback(30,[3])
		self.assets.append("cup")
		self.status[1] = "drinking"
		def f(x): 
			self.assets.remove("cup")
			self.status[1] = ""
		self.timers.append([200,f,[0]])


		
	def keyupdowncontrol(self,event,horse):
		
		if event.type == pygame.KEYDOWN:
			if event.key==pygame.K_DOWN:
				if self.status[1] == "":
					self.drink()
			
			if event.key==pygame.K_UP:
				if self.status[0] == "" :
					
					if abs((self.yo-10) - horse.yo)<10*self.s:
						self.mount(horse)
					else:
						settings.msg= ["CANNOT MOUNT ON SLOPE.",settings.msgt]
				elif self.status[0] == "mounted":
					self.dismount(horse)
		if event.type == pygame.KEYDOWN:
			if self.eventdelay <= 0:
				if event.key==pygame.K_LEFT:
					if not "bow" in self.status[1] and not "drinking" in self.status[1]:
						self.status[1] = "bow prepares"
						self.eventdelay=80	
		if event.type == pygame.KEYUP:
			
			if event.key==pygame.K_LEFT:
				if "bow" in self.status[1]:
					self.releasebow()
		

	def keyholdcontrol(self):	
		self.eventdelay -= self.eventdelay>0
		if pygame.key.get_pressed()[pygame.K_RIGHT]:
			self.walk()
		else:
			self.rest()
		if pygame.key.get_pressed()[pygame.K_LEFT] and (not "ing" in self.status[0]) and "bow" in self.status[1] and not "releasing" in self.status[1]:
			self.drawbow()
			
			
			
			
class Bird(Animal):
	def __init__(self,x,y):
		super(Bird,self).__init__(x,y)
		self.skel=[ [ -60, 5, 1],		
					[  30, 5, 2],#1
					[   0, 0, 2],
					[ 190,10, 2],
					[ -10, 8, 3],
					[ 150, 8, 2],#5
					[ -60,10, 5],
					[  50,10, 6],
					[ 150, 8, 2],
					[ -60,10, 8],
					[  50,10, 9],#10
					[-140, 8, 2],
					[ -30, 3,11],
					[  50, 5,12],
					[ -30, 3,11],
					[  50, 5,14] #15
				  ]
		self.ssk = copy.deepcopy(self.skel)			
		self.aspd = 0.1
			
		self.t = random.random()*math.pi*2	
			
		self.w1 = [-5,-5]
		self.w2 = [-3,-20]
		self.w3 = [-8,-30]
		self.t2 = 0
		self.v = [0,0]
		self.on = 0

		self.arrow = None

	def wingCoordToRL(self,n,w,lw=[0,0],lr=0,slr=0):
		self.skel[n][0] = -(180-(-math.degrees(math.atan2(w[1]-lw[1],w[0]-lw[0]))-slr+180-lr))
		self.skel[n][1] = math.sqrt((w[0]-lw[0])**2+(w[1]-lw[1])**2)

	def fly(self):
		s = self
		s.t += 1
		
		s.w1[1] = -1+u.trapwave(s.t*s.aspd)*3 
		s.w2[1] = -2+u.trapwave(s.t*s.aspd)*8 
		s.w3[1] = -1+u.trapwave(s.t*s.aspd+math.pi*0.2)*12
			
		s.w2[0] = -3+math.sin(s.t*s.aspd-math.pi*0.5)*2 
		s.w3[0] = -12+math.sin(s.t*s.aspd-math.pi*0.5)*3 
			
			
		s.wingCoordToRL(5,s.w1)
		s.wingCoordToRL(6,s.w2,s.w1,s.skel[5][0])
		s.wingCoordToRL(7,s.w3,s.w2,s.skel[6][0],s.skel[5][0])
		
		s.wingCoordToRL(8,s.w1)
		s.wingCoordToRL(9,s.w2,s.w1,s.skel[5][0])
		s.wingCoordToRL(10,s.w3,s.w2,s.skel[6][0],s.skel[5][0])			
			
			
		s.to(4,0,-0+math.sin(s.t*s.aspd+math.pi)*10) 
		s.to(1,0,10+math.sin(s.t*s.aspd)*10)
		
		s.to(12,0,-30)
		s.to(14,0,-30)
		s.to(1,1,3)

		
		s.to(13,0,50+math.sin(s.t*s.aspd)*10 + 10*noise.noise(s.t*s.aspd*0.01,1)-5)
		s.to(15,0,50+math.sin(s.t*s.aspd)*10 + 10*noise.noise(s.t*s.aspd*0.01,2)-5)

		s.x += s.v[0]*s.dir
		s.y += 0.5*s.v[1]+0.5*s.v[1]*(0.5*(math.sin(s.t*s.aspd)+1))
	
	def simpFly(self):
		s = self
		s.t += 1
		
		s.w1[1] = -1+u.trapwave(s.t*s.aspd)*3 
		s.w2[1] = -2+u.trapwave(s.t*s.aspd)*8 
		s.w3[1] = -1+u.trapwave(s.t*s.aspd+math.pi*0.2)*12
			
		s.w2[0] = -3+math.sin(s.t*s.aspd-math.pi*0.5)*2 
		s.w3[0] = -12+math.sin(s.t*s.aspd-math.pi*0.5)*3 
				
		s.wingCoordToRL(5,s.w1)
		s.wingCoordToRL(6,s.w2,s.w1,s.skel[5][0])
		s.wingCoordToRL(7,s.w3,s.w2,s.skel[6][0],s.skel[5][0])
					
		s.to(4,0,-0+math.sin(s.t*s.aspd+math.pi)*10) 
		s.to(1,0,10+math.sin(s.t*s.aspd)*10)
		
		s.to(1,1,3)

		s.x += s.v[0]*s.dir
		s.y += 0.5*s.v[1]+0.5*s.v[1]*(0.5*(math.sin(s.t*s.aspd)+1))	
		
	def fall(self):
		s = self
		s.v[0] = s.arrow.v[0]
		s.v[1] = s.arrow.v[1]
		s.x += s.v[0]
		s.y += s.v[1]

	def rest(self):
		
		s = self
		#s.t = -1 #math.pi
		s.t2 += 1
		s.to(5,0,20+180*2*((s.skel[5][0]>0)-0.5),10)
		s.to(6,0,-20+180*2*((s.skel[6][0]>0)-0.5),10)
		s.to(7,0,20-180*2*((s.skel[10][0]<0)-0.5),10)
		
		s.to(8,0,20+180*2*((s.skel[8][0]>0)-0.5),10)
		s.to(9,0,-20+180*2*((s.skel[9][0]>0)-0.5),10)
		s.to(10,0,20-180*2*((s.skel[10][0]<0)-0.5),10)

		s.to(12,0,30,10)
		s.to(14,0,30,10)
		s.to(13,0,100,10)
		s.to(15,0,100,10)
		
		noi = max(min((noise.noise(s.t2*s.aspd*0.5)-0.3)*50,1),-1)
		s.to(1,0,-10+noi*20,5)
		s.to(1,1,5-noi*2,5)
		s.to(4,0,-10+noi*10,5)
		
		s.x += s.v[0]*s.dir
		s.y += s.v[1]
		if s.y>=0:
			s.v[1] = 0
			s.v[0] = 0
			s.y = 0
		else:
			s.v[1] += 0.2*s.s
		if random.random() < 0.02 and s.v[1] == 0:
			s.v[1]=-1*s.s
			r = random.choice([1,1])
			s.v[0]+=0.5*r*s.s
			#s.dir = r
			
	
	
	def draw(self,surf):
		cd = []
		for i in range(len(self.skel)):
			cd.append(self.calcCoord(i)[:2])		
		s = self
		s.poly(surf,cd[3],cd[2],cd[5],
					[cd[5][0]-5,cd[5][1]])
		s.poly(surf,cd[5],cd[6],
					[cd[6][0]-8,cd[6][1]],
					[cd[5][0]-5,cd[5][1]])
		s.poly(surf,cd[6],[cd[6][0]-8,cd[6][1]],cd[7])
		s.poly(surf,cd[2],cd[5],cd[6])
		
		
		s.poly(surf,cd[3],cd[2],cd[8],
					[cd[8][0]-5,cd[8][1]])
		s.poly(surf,cd[8],cd[9],
					[cd[9][0]-8,cd[9][1]],
					[cd[8][0]-5,cd[8][1]])
		s.poly(surf,cd[9],[cd[9][0]-8,cd[9][1]],cd[10])
		s.poly(surf,cd[2],cd[8],cd[9])


		
		
			
		s.poly(surf,cd[2],[(cd[2][0]+cd[3][0])/2,(cd[2][1]+cd[3][1])/2-2],cd[3],cd[11],[cd[11][0]+5,cd[11][1]])
		s.poly(surf,[(cd[3][0]+cd[4][0])/2,(cd[3][1]+cd[4][1])/2],cd[3],cd[11])
		s.poly(surf,cd[0],cd[1],cd[2])
		s.poly(surf,cd[11],[(cd[0][0]+cd[1][0])/2,(cd[0][1]+cd[1][1])/2],cd[1],cd[2])
			
		s.line(surf,cd[11],cd[12],3)
		s.line(surf,cd[11],cd[14],3)
		
		s.line(surf,cd[3],cd[4],2)
		
		s.line(surf,cd[12],cd[13])
		s.line(surf,cd[14],cd[15])
	def simpDraw(self,surf):
		cd = []
		for i in range(len(self.skel)-3):
			cd.append(self.calcCoord(i)[:2])		
		s = self

		s.poly(surf,cd[3],cd[2],cd[5],
					[cd[5][0]-5,cd[5][1]])
		s.poly(surf,cd[5],cd[6],
					[cd[6][0]-8,cd[6][1]],
					[cd[5][0]-5,cd[5][1]])
		s.poly(surf,cd[6],[cd[6][0]-8,cd[6][1]],cd[7])
		#s.poly(surf,cd[2],cd[5],cd[6])	
			
		s.poly(surf,cd[4],cd[11],cd[0],cd[1],cd[2],cd[3])
			
	
	
class Crane(Bird):
	def __init__(self,x,y):
		super(Crane,self).__init__(x,y)
		self.skel=[ [ -5, 8, 1],		
					[  30,10, 2],#1
					[   0, 0, 2],
					[ 190,10, 2],
					[ -10, 5, 3],
					[ 150, 8, 2],#5
					[ -60,10, 5],
					[  50,10, 6],
					[ 150, 8, 2],
					[ -60,10, 8],
					[  50,10, 9],#10
					[-140, 8, 2],
					[ -30, 3,11],
					[  50,10,12],
					[ -30, 3,11],
					[  50,10,14] #15
				  ]		
		self.t = random.random()*math.pi*2	
	def fly(self):
		
		s = self
		s.t += 1
		
		s.w1[1] = -1+u.trapwave(s.t*s.aspd)*3 
		s.w2[1] = -2+u.trapwave(s.t*s.aspd)*8 
		s.w3[1] = -1+u.trapwave(s.t*s.aspd+math.pi*0.2)*12
			
		s.w2[0] = -3+math.sin(s.t*s.aspd-math.pi*0.5)*2 
		s.w3[0] = -5+math.sin(s.t*s.aspd-math.pi*0.5)*3 
			
			
		s.wingCoordToRL(5,s.w1)
		s.wingCoordToRL(6,s.w2,s.w1,s.skel[5][0])
		s.wingCoordToRL(7,s.w3,s.w2,s.skel[6][0],s.skel[5][0])
		
		s.wingCoordToRL(8,s.w1)
		s.wingCoordToRL(9,s.w2,s.w1,s.skel[5][0])
		s.wingCoordToRL(10,s.w3,s.w2,s.skel[6][0],s.skel[5][0])			
			
			
		s.to(4,0,-0+math.sin(s.t*s.aspd+math.pi)*10) 
		s.to(1,0,-5+math.sin(s.t*s.aspd)*1)
		
		s.to(12,0,-40)
		s.to(14,0,-40)
		
		s.to(13,0,10+math.sin(s.t*s.aspd)*5 + 10*noise.noise(s.t*s.aspd*0.01,1)-5)
		s.to(15,0,10+math.sin(s.t*s.aspd)*5 + 10*noise.noise(s.t*s.aspd*0.01,2)-5)

		#s.x += s.v[0]*s.dir
		s.y += 0.2*self.s*math.sin(s.t*s.aspd+math.pi)#30.5*s.v[1]+0.5*s.v[1]*(0.5*(math.sin(s.t*s.aspd)+1))
		
	def draw(self,surf):
		cd = []
		for i in range(len(self.skel)):
			cd.append(self.calcCoord(i)[:2])		
		s = self
		s.poly(surf,cd[3],cd[2],cd[5],
					[cd[5][0]-5,cd[5][1]])
		s.poly(surf,cd[5],cd[6],
					[cd[6][0]-8,cd[6][1]],
					[cd[5][0]-5,cd[5][1]])
		s.poly(surf,cd[6],[cd[6][0]-8,cd[6][1]],cd[7])
		s.poly(surf,cd[2],cd[5],cd[6])
		
		
		s.poly(surf,cd[3],cd[2],cd[8],
					[cd[8][0]-5,cd[8][1]])
		s.poly(surf,cd[8],cd[9],
					[cd[9][0]-8,cd[9][1]],
					[cd[8][0]-5,cd[8][1]])
		s.poly(surf,cd[9],[cd[9][0]-8,cd[9][1]],cd[10])
		s.poly(surf,cd[2],cd[8],cd[9])
		
			
		s.poly(surf,cd[2],[(cd[2][0]+cd[3][0])/2,(cd[2][1]+cd[3][1])/2-2],cd[3],cd[11],[(cd[2][0]+cd[1][0])/2,(cd[2][1]+cd[1][1])/2])
		s.poly(surf,[(cd[3][0]+cd[4][0])/2,(cd[3][1]+cd[4][1])/2],cd[3],cd[11])
		s.poly(surf,cd[1],cd[2],[cd[2][0],cd[2][1]+2])
		s.poly(surf,cd[0],cd[1],[(cd[0][0]+cd[1][0])/2,(cd[0][1]+cd[1][1])/2-2])
		#s.line(surf,cd[2],cd[1],1)
		#s.poly(surf,cd[0],cd[1],cd[2])
		#s.poly(surf,cd[11],[(cd[0][0]+cd[1][0])/2,(cd[0][1]+cd[1][1])/2],cd[1],cd[2])
			
		s.line(surf,cd[11],cd[12],1)
		s.line(surf,cd[11],cd[14],1)
		
		s.poly(surf,cd[3],cd[4],cd[11])
		#s.line(surf,cd[3],cd[4],2)
		
		s.line(surf,cd[12],cd[13],0.5)
		#s.line(surf,cd[14],cd[15])	
	
	
	
	
	
	
			
			
if __name__ == "__main__":
	settings.init()
	screen = pygame.display.set_mode([480,320])
	
	horse = Horse(100,0)
	horse2 = Horse(100,0)
	horse2.s = 2.5
	horse2.aspd = 0.1	
	
	
	deer = Deer(220,0,s=4)
	deer.yo = 150
	
	arrows = []
	man = Man(200,0)
	man.arrows = arrows
	horse2.yo=140
	man.yo=160
	man.s = 2#0.7
	man.walk()
	
	bird = Crane(200,0)
	bird.s = 5
	bird.aspd = 0.05
	bird.yo = 250

	bird2 = Crane(200,0)
	bird2.s = 5
	bird2.aspd = 0.05
	bird2.yo = 120

	
	birds = []
	

	for i in range(0,10):
		b = Bird(random.randrange(150,300),0)
		b.s = 0.5
		b.aspd = 0.3
		b.yo = 176
		b.dir = random.choice([1,-1])
		birds.append(b)
	
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			man.keyupdowncontrol(event,horse2)

						
						
		man.keyholdcontrol()
		screen.fill([240,240,240])

		
		#horse.drawSkel(screen)		
		#horse.walk()

		#horse2.draw(screen)
		man.animate()
		horse2.animate()
		#bird.draw(screen)
		bird.fly()

		#bird2.drawSkel(screen)
		bird2.fly()
		
		#print(man.status)
		#man.draw(screen)
		#man.drawSkel(screen)
		for b in birds:
			if abs(man.x - b.x) < 100 and random.random()<0.05 and b.on == 0:
				b.on = 1
				ra = math.pi/6.0+random.random()*math.pi/6.0*1.5
				rl = random.choice([2,3,4])
				b.v=[rl*math.cos(ra),-rl*math.sin(ra)]
			if b.on == 1:
				b.simpFly()
			else:
				b.rest()
		
		
		#bird.drawSkel(screen)
		#bird.s = math.sin(bird.t*0.01)*5+5
		#for b in birds:
			#b.simpDraw(screen)
		deer.walk()
		if pygame.key.get_pressed()[pygame.K_RIGHT]:
			horse2.walk()
			
			for b in birds:
				b.x -= 0.5
			#print deer.t

		else:
			horse2.rest()
			deer.rest()
		deer.draw(screen)


		for a in arrows:
			a.fly()
			a.draw(screen)

			#man.mount(horse2)	
		#pygame.display.set_icon(screen)
		pygame.display.flip()
	
	
