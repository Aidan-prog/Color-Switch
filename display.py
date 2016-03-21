import pygame, math

pygame.init()
pygame.font.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 128, 64
SCREEN_SCALE = 4
DISPLAY_WIDTH, DISPLAY_HEIGHT = SCREEN_WIDTH*SCREEN_SCALE, SCREEN_HEIGHT*SCREEN_SCALE
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Color Switch")
clock = pygame.time.Clock()
BLACK = (0,0,0)
WHITE = (255,255,255)
radius = 10

def handle_events():
	global radius
	for e in pygame.event.get():
		if(e.type == pygame.KEYDOWN):
			if(e.key == pygame.K_ESCAPE):
				return False
			elif(e.key == pygame.K_LEFT):
				radius-=1
			elif(e.key == pygame.K_RIGHT):
				radius+=1
		if(e.type == pygame.QUIT):
			return False
	return True
	
def draw_pixel(x,y, black=True):
	if(black):
		pygame.draw.rect(display, BLACK, (x*SCREEN_SCALE, y*SCREEN_SCALE, SCREEN_SCALE, SCREEN_SCALE))
	else:
		pygame.draw.rect(display, WHITE, (x*SCREEN_SCALE, y*SCREEN_SCALE, SCREEN_SCALE, SCREEN_SCALE))
		
def sgn(x):
	if(x == 0):
		return 0
	return (x / math.fabs(x))
		
def draw_line(x0, y0, x1, y1):
	dX = x1-x0
	dY = y1-y0
	error = 0
	if(dX == 0):
		dErr = 0
		for x in range(int(x0), int(x1)):
			draw_pixel(x,y0)
	elif(dy == 0):
		
	else:
		dErr = math.fabs(dY/dX)
	y = 0
	for x in range(int(x0), int(x1)):
		draw_pixel(x,y)
		error+=dErr
		while(error >= 0.5):
			draw_pixel(x,y)
			y+= sgn(dY)
			error -= 1
		
def draw_circle(cX, cY, rad, black=True):
	x,y = rad, 0
	decisionOver2 = 1 - x  # Decision criterion divided by 2 evaluated at x=r, y=0

	while(y <= x):
		draw_pixel( x + cX,  y + cY) #Octant 1
		draw_pixel(-x + cX,  y + cY) #Octant 4
		draw_pixel( y + cX,  x + cY) #Octant 2
		draw_pixel(-y + cX,  x + cY) #Octant 3
		draw_pixel( x + cX, -y + cY) #Octant 7
		draw_pixel(-x + cX, -y + cY) #Octant 5
		draw_pixel( y + cX, -x + cY) #Octant 8
		draw_pixel(-y + cX, -x + cY) #Octant 6
		y+=1
		if (decisionOver2<=0):
			decisionOver2 += 2 * y + 1   # Change in decision criterion for y -> y+1
		else:
			x-=1
			decisionOver2 += 2 * (y - x) + 1   # Change for y -> y+1, x -> x-1
		
def draw_filled_circle(cX, cY, rad, black=True):
	x, y = rad, 0
	decisionOver2 = 1 - x 
	while(y<=x):
		#draw_pixel( x + cX,  y + cY) #Octant 1
		#draw_pixel(-x + cX,  y + cY) #Octant 4
		
		draw_line(-x+cX, 32, x+cX, 32)
		#draw_pixel( y + cX,  x + cY) #Octant 2
		#draw_pixel(-y + cX,  x + cY) #Octant 3
		draw_pixel( x + cX, -y + cY) #Octant 7
		draw_pixel(-x + cX, -y + cY) #Octant 5
		draw_pixel( y + cX, -x + cY) #Octant 8
		draw_pixel(-y + cX, -x + cY) #Octant 6
		y+=1
		if (decisionOver2<=0):
			decisionOver2 += 2 * y + 1   # Change in decision criterion for y -> y+1
		else:
			x-=1
			decisionOver2 += 2 * (y - x) + 1   # Change for y -> y+1, x -> x-1
		
		
while(handle_events()):
	clock.tick(60)
	display.fill(WHITE)
	
	draw_filled_circle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, radius)
	draw_line(0,64, 128, 64)
	
	pygame.display.flip()

pygame.quit()
