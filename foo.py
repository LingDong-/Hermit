class IRCReplyModule(object):

    activated=True
    moduleHandlerResultList=None
    moduleHandlerCommandlist=None
    modulename=""

    def __init__(self,modulename):
        self.modulename = modulename


class SimpleHelloWorld(IRCReplyModule):

     def __init__(self):
            super(SimpleHelloWorld,self).__init__('hello world')
            
            
class A(SimpleHelloWorld):
	def __init__(self):
		    super(A,self).__init__()        
            
a = SimpleHelloWorld()
b = A()

"""
def Icon1():
	global icon
	color = (70,69,63)
	icondeer = creature.Deer(240,0,color,7.6)
	icondeer.yo = 240
	icondeer.t = 50
	icondeer.walk()
	icon.fill(COLOR_KEY)
	icondeer.draw(icon)
	iconman = creature.Man(320,0)
	iconman.yo=240
	iconman.s=7
	iconman.color=color
	iconman.to(4,0,90,1)
	iconman.to(5,0,-160,1)
	iconman.to(6,0,-80,1)
	iconman.to(7,0,0,1)
	iconman.to(4,1,10,1)
	iconman.to(8,0,110,1)
	iconman.to(9,0,-110,1)	
	iconman.to(1,0,100,1)
	iconman.to(0,0,30,1)
	iconman.to(3,1,10,1)
	iconman.to(8,1,20,1)
	iconman.to(9,1,20,1)
	iconman.to(10,1,25,1)
	iconman.to(10,0,-15,1)
	iconman.assets=["bow","arrow"]
	iconman.draw(icon)
	pygame.display.set_icon(icon)
	"""
