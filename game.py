import pygame, pygame.gfxdraw, math

pygame.init()
pygame.font.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 500,500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Switch")
pygame.display.set_icon(pygame.image.load("H:\\Documents\\Programming\\Python\\test2\\color_switch.png"))

PURPLE = (140, 19, 251) 
RED = (255, 0, 128)
TEAL = (53, 226, 242)
YELLOW = (246, 223, 14)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
obstacles = list() 
stars = list()
MENU, GAMEPLAY, PAUSE, GAMEOVER = range(4)
score = 0
highscore = 0

font = pygame.font.Font(pygame.font.get_default_font(), 24)

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

cam = Camera() 
       
class Obstacle:
    def __init__(self, surface, x=250, y=150):
        self.x = x
        self.y = y
        self.rad = 220
        self.angle = 0
        self.surface = surface
        
    def update(self):
        self.angle+=1
        if(self.angle > 360):
            self.angle-=360
        
    def draw(self):
        #pygame.gfxdraw.arc(self.surface, self.x, self.y, 100, 0, 180, (255,255,255))
        x, y = (self.x-float(self.rad/2)+cam.x, self.y-float(self.rad/2)-cam.y)
        pygame.draw.arc(self.surface, PURPLE , (x, y, self.rad, self.rad), math.radians(0+self.angle) ,math.radians(90+self.angle), 25)
        pygame.draw.arc(self.surface, PURPLE , (x, y+1, self.rad, self.rad), math.radians(0+self.angle) ,math.radians(90+self.angle), 25)
        pygame.draw.arc(self.surface, YELLOW , (x, y, self.rad, self.rad), math.radians(90+self.angle) , math.radians(180+self.angle), 25)
        pygame.draw.arc(self.surface, YELLOW , (x, y+1, self.rad, self.rad), math.radians(90+self.angle) ,math.radians(180+self.angle), 25)
        pygame.draw.arc(self.surface, TEAL , (x, y, self.rad, self.rad), math.radians(180+self.angle) ,math.radians(270+self.angle), 25)
        pygame.draw.arc(self.surface, TEAL , (x, y+1, self.rad, self.rad), math.radians(180+self.angle) ,math.radians(270+self.angle), 25)
        pygame.draw.arc(self.surface, RED , (x, y, self.rad, self.rad), math.radians(270+self.angle) ,math.radians(360+self.angle), 25)
        pygame.draw.arc(self.surface, RED , (x, y+1, self.rad, self.rad), math.radians(270+self.angle) ,math.radians(360+self.angle), 25)
        
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
       
class ColorSwitch:
    def __init__(self, surface):
        self.x = 250
        self.y = 400
       
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
            if(star.y >= self.y-16):
                #print("ayy lmao")
                star.color = BLACK
                if(not star.dead):
                    score+=1
                star.dead = True
      
    def update(self):
        self.vel -= 0.5
        self.y -= self.vel
        if(cam.y >= self.y-SCREEN_HEIGHT/2):
            cam.y = self.y-SCREEN_HEIGHT/2
        self.collision_detection()
        
    def draw(self):
        x = int(self.x+cam.x)
        y = int(self.y-cam.y)
        # pygame.draw.circle(self.surface, (255,255,255), (x,y), self.rad)
        pygame.gfxdraw.aacircle(self.surface, x, y, self.rad, self.color)
        pygame.gfxdraw.filled_circle(self.surface, x, y, self.rad, self.color)
        
      
ball = Ball(screen)
for i in range(50):
    temp = Obstacle(screen, 250, -400*i)
    temp_star = Star(screen, 250, -400*i)
    obstacles.append(temp)
    stars.append(temp_star)

def handle_events():
    for e in pygame.event.get():
        if(e.type == pygame.QUIT):
            return False
        if(e.type == pygame.KEYDOWN):
            if(e.key == pygame.K_ESCAPE):
                return False
            elif(e.key == pygame.K_SPACE):
                ball.vel = 8
    return True

def draw_ui():
    screen.blit(font.render(str(score), True, WHITE), (10, 10))
    
while(handle_events()):
    clock.tick(60)
    screen.fill((20,20,20))
    draw_ui()
	
    for obstacle in obstacles:
        obstacle.update()
    for star in stars:
        star.update()
    ball.update()
	
    ball.draw()
    for obstacle in obstacles:
        obstacle.draw()
    for star in stars:
        star.draw()
    star.draw()
    
    pygame.display.flip()
    #pygame.display.set_icon(screen)
    
pygame.quit()
