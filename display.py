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
	
def draw_pixel(x,y, color=True):
	if(color):
		pygame.draw.rect(display, BLACK, (x*SCREEN_SCALE, y*SCREEN_SCALE, SCREEN_SCALE, SCREEN_SCALE))
	else:
		pygame.draw.rect(display, WHITE, (x*SCREEN_SCALE, y*SCREEN_SCALE, SCREEN_SCALE, SCREEN_SCALE))
		
def sgn(x):
	if(x == 0):
		return 0
	return (x / math.fabs(x))
		
def draw_line(x0, y0, x1, y1, color=True):
	dX = x1-x0
	dY = y1-y0
	dErr = 0
	
	if(dX == 0):
		for y in range(int(y0), int(y1)):
			draw_pixel(x0,y, color)
		return
	elif(dY == 0):
		for x in range(int(x0), int(x1)):
			draw_pixel(x,y0, color)
		return
	else:
		dErr = dY/dX
		error = 0
		dErr = math.fabs(dY/dX)
	print("ran")
	y = 0
	for x in range(int(x0), int(x1)):
		draw_pixel(x,y, color)
		error+=dErr
		while(error >= 0.5):
			draw_pixel(x,y, color)
			y+= sgn(dY)
			error -= 1
		
def draw_circle(cX, cY, rad, color=True):
	x,y = rad, 0
	decisionOver2 = 1 - x  # Decision criterion divided by 2 evaluated at x=r, y=0

	while(y <= x):
		draw_pixel( x + cX,  y + cY, color) #Octant 1
		draw_pixel(-x + cX,  y + cY, color) #Octant 4
		draw_pixel( y + cX,  x + cY, color) #Octant 2
		draw_pixel(-y + cX,  x + cY, color) #Octant 3
		draw_pixel( x + cX, -y + cY, color) #Octant 7
		draw_pixel(-x + cX, -y + cY, color) #Octant 5
		draw_pixel( y + cX, -x + cY, color) #Octant 8
		draw_pixel(-y + cX, -x + cY, color) #Octant 6
		y+=1
		if (decisionOver2<=0):
			decisionOver2 += 2 * y + 1   # Change in decision criterion for y -> y+1
		else:
			x-=1
			decisionOver2 += 2 * (y - x) + 1   # Change for y -> y+1, x -> x-1
		
def draw_filled_circle(cX, cY, rad, color=True):
	x, y = rad, 0
	decisionOver2 = 1 - x 
	while(y<=x):
		
		draw_line(-x+cX, y+cY, x+cX, y+cY, color)
		draw_line(-y+cX, -x+cY, y+cX, -x+cY, color)
		draw_line(-x+cX, -y+cY, x+cX, -y+cY, color)
		draw_line(-y+cX, x+cY, y+cX, x+cY, color)
		
		draw_pixel( x + cX,  y + cY, color) #Octant 1
		draw_pixel(-x + cX,  y + cY, color) #Octant 4
		draw_pixel( y + cX,  x + cY, color) #Octant 2
		draw_pixel(-y + cX,  x + cY, color) #Octant 3
		draw_pixel( x + cX, -y + cY, color) #Octant 7
		draw_pixel(-x + cX, -y + cY, color) #Octant 5
		draw_pixel( y + cX, -x + cY, color) #Octant 8
		draw_pixel(-y + cX, -x + cY, color) #Octant 6
		y+=1
		if (decisionOver2<=0):
			decisionOver2 += 2 * y + 1   # Change in decision criterion for y -> y+1
		else:
			x-=1
			decisionOver2 += 2 * (y - x) + 1   # Change for y -> y+1, x -> x-1
		
		
while(handle_events()):
	clock.tick(60)
	display.fill(BLACK)
	
	draw_filled_circle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, radius, False)
	#draw_line(0,63, 128, 63)
	#draw_pixel(123,63)
	
	pygame.display.flip()

pygame.quit()
