
import pygame
import sys
import math
import utilities as u
import copy
import random
import noise
import numpy as np

pygame.init()

def filter(array,t = 0):

	twave = math.sin(t*0.0005+1)
	for x in np.nditer(array[0],op_flags=['readwrite'],flags = ['external_loop']):
		x[...]= (x-35+twave*45)/(1.3-twave*0.3)

	for x in np.nditer(array[1],op_flags=['readwrite'],flags = ['external_loop']):
		x[...] = (x-35+twave*44)/(1.3-twave*0.3)

	for x in np.nditer(array[2],op_flags=['readwrite'],flags = ['external_loop']):
		x[...] = (x-25+twave*25)/(1.3-twave*0.3)




if __name__ == "__main__":
	screen = pygame.display.set_mode([640,320])
	clock = pygame.time.Clock()
	print screen.get_bitsize()
	t = 0
	while 1:
		t += 100
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		array = []
		screen.fill([200,200,200])

		u.circle(screen,(100,100,100),[50,50],50)

		clock.tick()
		u.text(screen,10,10,"FPS: %.1f" % clock.get_fps(),(150,150,150))



		array = [pygame.surfarray.pixels_red(screen),pygame.surfarray.pixels_green(screen),pygame.surfarray.pixels_blue(screen)]

		filter(array,t)
		#pygame.surfarray.blit_array(screen,array)
		pygame.display.flip()
