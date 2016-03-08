import pygame, pygame.gfxdraw, math, random

pygame.init()
pygame.font.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 500,700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Switch")
pygame.display.set_icon(pygame.image.load("H:\\Documents\\Programming\\Python\\test2\\color_switch.png"))
#pygame.display.set_icon(pygame.image.load("color_switch.png"))
#pygame.display.set_icon(pygame.image.load("C:\\Users\\Tupou\\Documents\\Programming\\Python\\Color Switch\\color_switch.png"))

PURPLE = (140, 19, 251)
RED = (255, 0, 128)
TEAL = (53, 226, 242)
YELLOW = (246, 223, 14)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
obstacles = list() 
stars = list()
colorswitches = list()
MENU, GAMEPLAY, PAUSE, GAMEOVER = range(4)
gamestate = MENU
score = 0
highscore = 0

font = pygame.font.Font(pygame.font.get_default_font(), 24)
menu_font = pygame.font.Font(pygame.font.get_default_font(), 60)

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

cam = Camera() 
       
class Obstacle:
    def __init__(self, surface, x=250, y=150, rad=220, angle = 0, vel = 1):
        self.x = x
        self.y = y
        self.rad = rad
        self.angle = angle
        self.surface = surface
        self.vel = vel
        self.thickness = 25
        
    def update(self):
        self.angle+=self.vel
        if(self.angle > 360):
            self.angle-=360
        elif(self.angle <= 0):
            self.angle+=360
        
    def draw(self):
        #pygame.gfxdraw.arc(self.surface, self.x, self.y, 100, 0, 180, (255,255,255))
        x, y = (self.x-float(self.rad/2)-cam.x, self.y-float(self.rad/2)-cam.y)
        x, y = int(x), int(y)
        thick = self.thickness
        pygame.draw.arc(self.surface, PURPLE , (x, y, self.rad, self.rad), math.radians(0+self.angle) ,math.radians(90+self.angle), thick)
        pygame.draw.arc(self.surface, PURPLE , (x, y+1, self.rad, self.rad), math.radians(0+self.angle) ,math.radians(90+self.angle), thick)
        pygame.draw.arc(self.surface, YELLOW , (x, y, self.rad, self.rad), math.radians(90+self.angle) , math.radians(180+self.angle), thick)
        pygame.draw.arc(self.surface, YELLOW , (x, y+1, self.rad, self.rad), math.radians(90+self.angle) ,math.radians(180+self.angle), thick)
        pygame.draw.arc(self.surface, TEAL , (x, y, self.rad, self.rad), math.radians(180+self.angle) ,math.radians(270+self.angle), thick)
        pygame.draw.arc(self.surface, TEAL , (x, y+1, self.rad, self.rad), math.radians(180+self.angle) ,math.radians(270+self.angle), thick)
        pygame.draw.arc(self.surface, RED , (x, y, self.rad, self.rad), math.radians(270+self.angle) ,math.radians(360+self.angle), thick)
        pygame.draw.arc(self.surface, RED , (x, y+1, self.rad, self.rad), math.radians(270+self.angle) ,math.radians(360+self.angle), thick)
        
        #pygame.gfxdraw.aacircle(self.surface, int(self.x), int(self.y), int(self.rad/2), (20,20,20))
        pygame.gfxdraw.aacircle(self.surface, int(self.x-cam.x), int(self.y-cam.y), int(self.rad/2)+1, (20,20,20))
        pygame.gfxdraw.aacircle(self.surface, int(self.x-cam.x), int(self.y-cam.y), int(self.rad/2), (20,20,20))
        pygame.gfxdraw.aacircle(self.surface, int(self.x-cam.x), int(self.y-cam.y), int(self.rad/2)-thick-1, (20,20,20))
        pygame.gfxdraw.aacircle(self.surface, int(self.x-cam.x), int(self.y-cam.y), int(self.rad/2)-thick, (20,20,20))
        
        
class Star:
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.surface = surface
        self.color = WHITE
        self.dead = False
        self.dead_counter = 0
        
    def update(self):
        if(self.dead and self.dead_counter < 40):
            self.dead_counter+=1
        elif(self.dead):
            stars.remove(self)
        
    def draw(self):
        x,y = self.x-cam.x,self.y-cam.y
        if(not self.dead):
            points = ((x,y-16),(x-7,y-5), (x-20,y-3), (x-11,y+8), (x-13, y+21), (x, y+16), (x+13, y+21), (x+11, y+8), (x+20, y-3), (x+7,y-5))
            pygame.gfxdraw.aapolygon(self.surface, points, self.color)
            pygame.gfxdraw.filled_polygon(self.surface, points, self.color) 
        else:
            self.surface.blit(font.render("+1", True, (255-self.dead_counter*5, 255-self.dead_counter*5, 255-self.dead_counter*5)), (x-10,y-self.dead_counter))
      
def draw_pie(x, y, rad, s_angle, e_angle, color):
    points = [(x,y)]
    for n in range(s_angle, e_angle+1):
        tx = x + int(rad*math.cos(math.radians(n)))
        ty = y + int(rad*math.sin(math.radians(n)))
        points.append((tx, ty))
    points.append((x,y))
    if(len(points)>2):
        pygame.gfxdraw.aapolygon(screen, points, color)
        pygame.gfxdraw.filled_polygon(screen, points, color)
        #pygame.draw.polygon(screen, RED, points)
      
class ColorSwitch:
    def __init__(self, surface, x, y):
        self.x = x
        self.y = y
        self.surface = surface
        self.rad = 22
        
    def draw(self):
        x, y = int(self.x-cam.x), int(self.y-cam.y)
        draw_pie(x, y, self.rad, 0, 90, RED)
        draw_pie(x, y, self.rad, 90, 180, TEAL)
        draw_pie(x, y, self.rad, 180, 270, YELLOW)
        draw_pie(x, y, self.rad, 270, 360, PURPLE)
        pygame.gfxdraw.aacircle(self.surface, x, y,self.rad-1, (20,20,20))
        pygame.gfxdraw.aacircle(self.surface, x, y,self.rad, (20,20,20))
        
        
       
class Ball:
    def __init__(self, surface):
        self.x = 250
        self.y = 400
        self.rad = 10
        self.surface = surface
        self.vel = 0
        self.color = YELLOW
        
    def collision_detection(self):
        global score   
        x, y = self.x-cam.x, self.y-cam.y
        for star in stars:
            if(star.y+16 >= self.y):
                print(star.y)
                star.color = BLACK
                if(not star.dead):
                    score+=1
                    print("+1 score")
                star.dead = True
				
        for obstacle in obstacles:
            if(obstacle.y+int(obstacle.rad/2) >= self.y and obstacle.y+int(obstacle.rad/2)-25 <= self.y):
                if(self.color != YELLOW and obstacle.angle > 90 and obstacle.angle <= 180):
                    self.die()
                elif(self.color != PURPLE and obstacle.angle > 180 and obstacle.angle <= 270):
                    self.die()
                elif(self.color != RED and obstacle.angle > 270 and obstacle.angle <= 360):
                    self.die()
                elif(self.color != TEAL and obstacle.angle <= 90):
                    self.die()
            elif(obstacle.y-(obstacle.rad/2)+25 >= self.y-self.rad and obstacle.y-(obstacle.rad/2) <= self.y):
                if(self.color != RED and obstacle.angle > 90 and obstacle.angle <= 180):
                    self.die()
                elif(self.color != TEAL and obstacle.angle > 180 and obstacle.angle <= 270):
                    self.die()
                elif(self.color != YELLOW and obstacle.angle > 270 and obstacle.angle <= 360):
                    self.die()
                elif(self.color != PURPLE and obstacle.angle <= 90):
                    self.die()
               
        for cs in colorswitches:
            if(cs.y >= self.y-self.rad*2):
                rand = random.randint(0,3)
                if(rand == 0):
                    self.color = PURPLE
                elif(rand == 1):
                    self.color = RED
                elif(rand == 2):
                    self.color = TEAL
                elif(rand == 3):
                    self.color = YELLOW
                colorswitches.remove(cs)
             
    def die(self):
        global score, highscore, gamestate
        gamestate = GAMEOVER
        if(score > highscore):
            highscore = score
             
    def update(self):
        self.vel -= 0.5
        self.y -= self.vel
        if(cam.y >= self.y-SCREEN_HEIGHT/2):
            cam.y = self.y-SCREEN_HEIGHT/2
        self.collision_detection()
        
    def draw(self):
        x = int(self.x-cam.x)
        y = int(self.y-cam.y)
        if(self.y > 10000):
            self.y = 9000
        pygame.gfxdraw.aacircle(self.surface, x, y, self.rad, self.color)
        pygame.gfxdraw.filled_circle(self.surface, x, y, self.rad, self.color)
        
      
ball = Ball(screen)
color_switch = ColorSwitch(screen, SCREEN_WIDTH/2, 250)

'''for i in range(20):
    temp = Obstacle(screen, SCREEN_WIDTH/2, -400*i)
    temp_star = Star(screen, SCREEN_WIDTH/2, -400*i)
    obstacles.append(temp)
    stars.append(temp_star)'''

def restart(): 
    global cam, ball, obstacles, score, stars
    cam = Camera()
    ball = Ball(screen)
    del stars[:]
    del obstacles[:]
    del colorswitches[:]
    for i in range(20):
        temp = Obstacle(screen, SCREEN_WIDTH/2, -450*i)
        temp_star = Star(screen, SCREEN_WIDTH/2, -450*i)
        temp_colorswitch = ColorSwitch(screen, SCREEN_WIDTH/2, -450*i+250)
        obstacles.append(temp)
        stars.append(temp_star)
        colorswitches.append(temp_colorswitch)
        
    score = 0
    
def handle_events():
    global gamestate
    for e in pygame.event.get():
        if(e.type == pygame.QUIT):
            return False
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                return False
            elif(e.key == pygame.K_SPACE):
                if(gamestate == GAMEPLAY):
                    ball.vel = 8
                elif(gamestate == GAMEOVER):
                    restart()
                    gamestate = GAMEPLAY
                elif(gamestate == MENU):
                    restart()
                    gamestate = GAMEPLAY
    return True

def draw_ui():
    screen.blit(font.render(str(score), True, WHITE), (10, 10))
    
x, y = int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)
menu_obstacle = Obstacle(screen, x, y,200, 45)
menu_obstacle2 = Obstacle(screen, x, y,250, 45+180,-1)
menu_obstacle3 = Obstacle(screen, x, y,310, 45+90)
menu_obstacle.thickness = 15
menu_obstacle2.thickness = 20

title_obstacle = Obstacle(screen, 210, 65, 50, 90)
title_obstacle2 = Obstacle(screen, 310, 65, 50, 0, -1)
title_obstacle.thickness = 7
title_obstacle2.thickness = 7


def draw_menu():
    
    screen.blit(menu_font.render("C    L    R", True, WHITE), (130, 40))
    screen.blit(menu_font.render("SWITCH", True, WHITE), (130, 100))

    menu_obstacle.update()
    menu_obstacle2.update()
    menu_obstacle3.update()
    title_obstacle.update()
    title_obstacle2.update()
    
    menu_obstacle.draw()
    menu_obstacle2.draw()
    menu_obstacle3.draw()
    pygame.draw.circle(screen, (70,70,70), (x,y), 80)
    points = ((x-20, y-40), (x-20, y+40), (x+35, y))
    pygame.gfxdraw.aapolygon(screen, points, WHITE)
    pygame.gfxdraw.filled_polygon(screen, points, WHITE)
    pygame.gfxdraw.aacircle(screen, x, y, 155, (20,20,20))
    pygame.gfxdraw.aacircle(screen, x, y, 156, (20,20,20))
    pygame.gfxdraw.aacircle(screen, x, y, 130, (20,20,20))
    title_obstacle.draw()
    title_obstacle.y-=1
    title_obstacle.draw()
    title_obstacle.y+=1
    pygame.gfxdraw.aacircle(screen, 210, 65, 27, (20,20,20))
    title_obstacle2.draw()
    title_obstacle2.y-=1
    title_obstacle2.draw()
    title_obstacle2.y+=1
    #ball.draw()
    
def draw_game_over():
    #screen.blit(font.render("GAME OVER", True, WHITE), (SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2))
    screen.blit(font.render("S C O R E", True, WHITE), (SCREEN_WIDTH/2-50, 120))
    screen.blit(menu_font.render(str(score), True, WHITE), (SCREEN_WIDTH/2-10, 150))
    screen.blit(font.render("B E S T   S C O R E", True, WHITE), (SCREEN_WIDTH/2-100, 250))
    screen.blit(menu_font.render(str(highscore), True, WHITE), (SCREEN_WIDTH/2-10, 290))
    
while(handle_events()):
    clock.tick(80)
    screen.fill((20,20,20))
    if(gamestate == MENU):
        draw_menu()
    elif(gamestate == GAMEPLAY):
        draw_ui()
        
        for obstacle in obstacles:
            obstacle.update()
        ball.update()
        for star in stars:
            star.update()
        
        for obstacle in obstacles:
            if(obstacle.y+obstacle.rad/2-cam.y >= 0 and obstacle.y-obstacle.rad/2-cam.y <= SCREEN_HEIGHT):
                obstacle.draw()
        for star in stars:
            if(star.y+13-cam.y >= 0 and star.y-13-cam.y <= SCREEN_HEIGHT):
                star.draw()
        for cs in colorswitches:
            cs.draw()
        ball.draw()
        
    elif(gamestate == GAMEOVER):
        draw_game_over()
        
    pygame.display.flip()
    
pygame.quit()
