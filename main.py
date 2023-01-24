import pygame
import math
import random
import os

class Ball():
    def __init__(self,screen):
        self.screen = screen
        self.ball_image= pygame.image.load(os.path.join('assets', 'ball.png')).convert_alpha()
        resize_ball = self.ball_image.get_rect()
        self.ball_image = pygame.transform.scale(self.ball_image,(resize_ball.width //2, resize_ball.height //2))
        self.x,self.y,self.xi,self.yi=0,0,0,0
        self.frameNum=9
        self.mark=0
        self.points=0
    def draw(self):
        if self.frameNum==9:
            return
        if self.frameNum==1:
            dx,dy=(350-self.x),(50-self.y)
            self.xi=dx//6
            self.yi=dy//6
            distance=math.sqrt((dx**2)+(dy**2))
            hit_rate=int(distance//100)
            if random.randint(1,hit_rate+1)==1:
                self.mark=1
            else:
                self.mark=0
        if self.frameNum>=1 and self.frameNum<6:
            self.x+=self.xi
            self.y+=self.yi
            self.frameNum+=1



        elif self.frameNum==6:
            self.x=350
            self.frameNum+=1
            if self.mark==1:
                self.y=90
            else:
                self.y=70


        else:
            if self.mark==0:
                if self.xi>=0:
                    self.x+=30
                else:
                    self.x-=30
            self.y+=25
            self.frameNum+=1
        self.screen.blit(self.ball_image, (self.x, self.y))
        if self.frameNum==9 and self.mark==1:
            self.points+=1

class Defender():
    def __init__(self,screen):
        self.screen=screen
        self.images=[]
        for i in range(2):
            defender_image = pygame.image.load('assets/'+str(i+16)+'.png').convert_alpha()
            resize_defender=defender_image.get_rect()
            defender_image = pygame.transform.scale(defender_image, (resize_defender.width//2, resize_defender.height//2))
            self.images.append(defender_image)
        self.frameNum=0
        self.x,self.y=400,320
        self.ShooterX, self.ShooterY= 0, 0
        self.ShooterFrameNum=0
        self.rect=None
    def draw(self):
        p=self.images[self.frameNum]
        if self.ShooterX-self.x<0:
            p=pygame.transform.flip(p,True,False)
        dx,dy= self.ShooterX - self.x, self.ShooterY - self.y
        dist=math.sqrt((dx**2)+(dy**2))
        dx1,dy1=0,0
        if dist>400:
            self.x,self.y=400,300
        elif self.ShooterFrameNum<4:
            if abs(dx)<abs(dy):
                d=abs(dx/dy)
                dy1=7

                dx1=int((dy1*d)//1)
            else:
                d=abs(dy/dx)
                dx1=7
                dy1=int((dx1*d)//1)
        if dx<0:
            dx1=-dx1

        if dy<0:
            dy1=-dy1

        self.x+=dx1
        self.y+=dy1
        self.rect=self.screen.blit(p,(self.x,self.y))
        self.frameNum+=1
        if self.frameNum==2:
            self.frameNum=0

class Shooter():
    def __init__(self,screen):
        self.screen=screen
        self.images=[]
        for n in range(16):
            shooter_image = pygame.image.load('assets/'+str(n)+'.png').convert_alpha()
            resize_shooter=shooter_image.get_rect()
            shooter_image = pygame.transform.scale(shooter_image, (resize_shooter.width//2, resize_shooter.height//2))
            self.images.append(shooter_image)
        self.frameNum=0
        self.x,self.y=0,0
        self.mouseX,self.mouseY=0,0
        self.jumpUpOrDown=-10
        self.rect=None
    def dribble(self):
        dribble_animation=self.images[self.frameNum]
        if self.mouseX-self.x<0:
            dribble_animation=pygame.transform.flip(dribble_animation,True,False)
        self.x,self.y=self.mouseX,self.mouseY
        if self.x<1:
            self.x=1
        if self.x+90>width:
            self.x=width-90
        if self.y<230:
            self.y=230
        if self.y+120>height:
            self.y=height-120
        self.rect=self.screen.blit(dribble_animation,(self.x,self.y))
        self.frameNum+=1
        if self.frameNum==4:
            self.frameNum=0
    def jumpShot(self):
        jump_animation=self.images[self.frameNum]
        if self.x>width/2:
            jump_animation=pygame.transform.flip(jump_animation,True,False)
        self.screen.blit(jump_animation, (self.x, self.y))
        self.y+=self.jumpUpOrDown
        self.frameNum+=1
        if self.frameNum==9:
            self.jumpUpOrDown=10
        if self.frameNum==16:
            self.frameNum=0
            self.jumpUpOrDown=-10


pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d"%(200,40)
size = width, height = 800,600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Basketball")
bg_img = pygame.image.load(os.path.join('assets', 'court.png')).convert()
icon= pygame.image.load(os.path.join('assets', 'ball.png'))
pygame.display.set_icon(icon)

fclock = pygame.time.Clock()
fps = 10
shooter=Shooter(screen)
ball=Ball(screen)
defender=Defender(screen)
font1 = pygame.font.SysFont(' Cooper ', 40, True)
gameOver=False
running = True
LEFT = 1
RIGHT = 3
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION :
            shooter.mouseX, shooter.mouseY=event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                pos = pygame.mouse.get_pos()
                if shooter.frameNum<4:
                    shooter.frameNum=4
            if event.button == RIGHT and gameOver==True:
                gameOver=False
                ball.points=0
    screen.blit(bg_img, (0, 0))
    surface1=font1.render('Points:' + str(ball.points), True, [0, 0, 0])
    screen.blit(surface1, (20, 20))
    if gameOver==True:
        fclock.tick(fps)
        continue
    if shooter.frameNum>=4:
        shooter.jumpShot()
        if shooter.frameNum==8:
            ball.frameNum=1
            ball.x=shooter.x
            ball.y=shooter.y
    else:
        shooter.dribble()
    ball.draw()
    defender.ShooterX, defender.ShooterY= shooter.x, shooter.y
    defender.ShooterFrameNum=shooter.frameNum
    defender.draw()
    if shooter.frameNum<4:
        if shooter.rect.colliderect(defender.rect):
            gameOver=True
            surface2=font1.render('Please press Right Click to play again',True,[0, 0, 0])
            screen.blit(surface2, (20, 550))
    pygame.display.flip()
    fclock.tick(fps)
pygame.quit()
