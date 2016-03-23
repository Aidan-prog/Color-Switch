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
        
        
def draw_arc(cX, cY, rad, sAngle, eAngle, col=True):
    #sAngle = math.radians(sAngle)
    #eAngle = math.radians(eAngle)

    #Standard Midpoint Circle algorithm
    p = int((5 - rad * 4) / 4)
    x = 0
    y = rad
    draw_circle_points(cX, cY, x, y, sAngle, eAngle, col);
    while(x <= y):
        x+=1
        if (p < 0):
            p += 2 * x + 1;
        else:
            y-=1
            p += 2 * (x - y) + 1
        draw_circle_points(cX, cY, x, y, sAngle, eAngle, col)
        
def draw_circle_points(cX, cY, x, y, sAngle, eAngle, col=True):

    #Calculate the angle the current point makes with the circle center
    angle = int(math.degrees(math.atan2(y, x)))
    #draw the circle points as long as they lie in the range specified
    if (x < y):
        #draw point in range 0 to 45 degrees
        if (90 - angle >= sAngle and 90 - angle <= eAngle):
            draw_pixel(cX - y, cY - x, col)

            #draw point in range 45 to 90 degrees
            if (angle >= sAngle and angle <= eAngle):
                draw_pixel(cX - x, cY - y, col)

            #draw point in range 90 to 135 degrees
            if (180 - angle >= sAngle and 180 - angle <= eAngle):
                draw_pixel(cX + x, cY - y, col)

            #draw point in range 135 to 180 degrees
            if (angle + 90 >= sAngle and angle + 90 <= eAngle):
                draw_pixel(cX + y, cY - x, col)

            #draw point in range 180 to 225 degrees
            if (270 - angle >= sAngle and 270 - angle <= eAngle):
                draw_pixel(cX + y, cY + x, col)
                
            #draw point in range 225 to 270 degrees
            if (angle + 180 >= sAngle and angle + 180 <= eAngle):
                draw_pixel(cX + x, cY + y, col)

            #draw point in range 270 to 315 degrees
            if (360 - angle >= sAngle and 360 - angle <= eAngle):
                draw_pixel(cX - x, cY + y, col)

            #draw point in range 315 to 360 degrees
            if (angle + 270 >= sAngle and angle + 270 <= eAngle):
                draw_pixel(cX - y, cY + x, col)
    
x = int(SCREEN_WIDTH*(1/4))
y = int(SCREEN_HEIGHT/2)
vel = 0
radius = 3
   
def ball_jump():
    global x,y,vel
    vel = 4
    
def ball_draw():
    draw_filled_circle(int(x), int(y), radius, False)
    
def ball_update():
    global x,y,vel
    x+=vel
    vel-=0.5
    
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
            if(e.key == pygame.K_SPACE):
                ball_jump()
        if(e.type == pygame.QUIT):
            return False
    return True

while(handle_events()):
    clock.tick(30)
    display.fill(BLACK)
    
    #ball_update()
    
    draw_arc(SCREEN_WIDTH/2, SCREEN_HEIGHT/2,radius, 0, 180, False)
    
    #ball_draw()

    pygame.display.flip()

pygame.quit()
