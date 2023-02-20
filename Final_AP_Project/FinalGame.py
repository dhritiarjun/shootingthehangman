#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame as pg
import math
import random
import subprocess
import sys

pg.init()
pg.font.init()

# create a class for the Hangman (villain)
class KillerHangman():
    def __init__(self, images, start_pos):
        #get screen rect:
        self.screen_rect = screen.get_rect()
        
        #get image and mask from hangmanimage:
        self.image = images[0]
        self.mask = images[1]
        
        #set start buffer:
        startbuffer = 0
        
        #get hangman image rect:
        self.rect = self.image.get_rect(
            center=(start_pos[0], start_pos[1])
        )
        
        #set values for hangman:
        self.distance_above_player = 100 
        self.speed = 3
        self.bullet_color = (255,215,0)
        self.is_hit = False
        self.range_to_fire = False
        self.timer = 0.0
        self.bullets = [ ]
        self.dead = False
         
    
   # create a function for the hangman to move towards the player:

    def towardsplayer(self, player_rect):
        
        distancex = player_rect.x - self.rect.x
        distance2 = player_rect.y - self.distance_above_player  - self.rect.y
        
        #this code helps the next function move the hangman towards the player:
        p = math.sqrt((distancex) ** 2 + (distance2) ** 2)
        
        try:
            x = (distancex) / p
            y = (distance2) / p
            #(player_rect.y - self.distance_above_player)  - self.rect.y
        
        #Zero division error in case p is 0
        except ZeroDivisionError: 
            return False
        return (x,y)
           
    def update(self, dt, player):
        #this function updates the position of the hangman using the information gained above:
        
        #get the new position from function above:
        new_pos = self.towardsplayer(player.rect)
        
        # code beneath checks for the zero division error then moves the hangman accordinglu:
        if new_pos: 
            self.rect.x, self.rect.y = (self.rect.x + new_pos[0] * self.speed, self.rect.y + new_pos[1] * self.speed)
        
        #check whether the player can shoot the hangman using function further below, then shoots bullet:
        self.checkifattack(player)
        if self.range_to_fire:
            #timer between fires, so that our hangman doesnt shoot continuosly:
            if pg.time.get_ticks() - self.timer > 1500.0:
                self.timer = pg.time.get_ticks()
                self.bullets.append(Bullet(self.rect.center, self.bullet_color))
        self.bulletsupdate(player)
        
    def draw(self, surf):
        if self.bullets:
            
            #draw the bullet(s) onto the screen:
            for bullet in self.bullets:
                surf.blit(bullet.image, bullet.rect)
                
        #draw the hangman itself onto the screen:
        surf.blit(self.image, self.rect)
 

    def checkifattack(self, player):
        #this function checks if the hangman can shoot the player
        if player.rect.y >= self.rect.y: 
            try:
                offset_x =  self.rect.x - player.rect.x
                offset_y =  self.rect.y - player.rect.y
                
                #find angle between hangman and player
                d = int(math.degrees(math.atan(offset_x / offset_y)))
            
            #zerodivision error in case dividing by 0:
            except ZeroDivisionError:
                return
            
            #get absolute value of d and check if hangman would be able to shoot player
            if math.fabs(d) <= 15: 
                self.range_to_fire = True
            else:
                self.range_to_fire = False
                
    def bulletsupdate(self, player):
        if self.bullets:
            for obj in self.bullets[:]:
                #move bullets using function in Bullet class:
                obj.update('down')
                #check collision between bullet and player using mask: 
                if obj.rect.colliderect(player.rect):
                    self.bullets.remove(obj)
                    ######@#######################
                    def spawn_program_and_die(program, exit_code=0):
                        subprocess.Popen(program)
                        sys.exit(exit_code)
                    spawn_program_and_die(['pythonw', 'endscreen.py'])
                    pygame.quit()
                    sys.exit()
                    
                    
class Bullet:
    def __init__(self, loc, screen_rect):
        
        #get screen rect:
        self.screen_rect = screen_rect
        
        #create the bullet
        self.image = pg.Surface((2,5)).convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        
        #choose bullet color:
        self.image.fill((212,175,55))
        
        #get bullet rect:
        self.rect = self.image.get_rect(center=loc)
        
        #set bullet speed
        self.speed = 8
     
    def update(self,direction='up'):
        #move the bullet:
        if direction == 'down':
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
     
    def render(self, surf):
        #draw bullet onto game:
        surf.blit(self.image, self.rect)
     
    
class Player:
    def __init__(self, screen_rect):
        #get screen rect:
        self.screen_rect = screen_rect
        #get player image:
        self.image = pg.image.load('player.png').convert()
        #scale player image:
        self.image = pg.transform.scale(self.image, (100, 80))
        self.image.set_colorkey((255,0,255))
        #set image masl to help create better collision detection
        self.mask = pg.mask.from_surface(self.image)
        #get image rect:
        startbuffer = 100
        self.rect = self.image.get_rect(center=(screen_rect.centerx, screen_rect.centery + startbuffer))
        #set player values:
        self.dx = 300
        self.dy = 300
        self.bullets = []
        self.timer = 0.0
        self.delaybullet = 1000
        self.addbullet = False
        self.damagetreshold = 2

    def get_event(self, event):
        #shoot bullet:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if self.addbullet:
                    #shoot bullet from the center of the player image:
                    self.bullets.append(Bullet(self.rect.center, self.screen_rect))
                    #stop loop from reoccuring
                    self.addbullet = False
     
    def update(self, keys, dt, hangmanarr):
        
        #clamp_ip forces the player rect to stay within the screen rect
        self.rect.clamp_ip(self.screen_rect)
        
        #make player move using keys:
        if keys[pg.K_LEFT]:
            self.rect.x -= self.dx * dt
        if keys[pg.K_RIGHT]:
            self.rect.x += self.dx * dt
        if keys[pg.K_UP]:
            self.rect.y -= self.dy * dt
        if keys[pg.K_DOWN]:
            self.rect.y += self.dy * dt
        #check delay time:
        if pg.time.get_ticks()-self.timer > self.delaybullet:
            self.timer = pg.time.get_ticks()
            self.addbullet = True
            
         #check if we hit the hangman using function below:    
        self.check_bullet_collision(hangmanarr)
         
    def check_bullet_collision(self, hangmanarr):
        for bullet in self.bullets[:]:
            bullet.update()
            for e in hangmanarr:
                if bullet.rect.colliderect(e.rect):
                    offset_x =  bullet.rect.x - e.rect.x 
                    offset_y =  bullet.rect.y - e.rect.y
                    #remove hangman if hangman collides with bullet:
                    e.dead = True
                    #check mask overlap:
                    if e.mask.overlap(bullet.mask, (offset_x, offset_y)):
                        self.bullets.remove(bullet)
                        #break to avoid Valueerror
                        break
             
    def draw(self, surf):
        #draw all bullets on screen:
        for bullet in self.bullets:
            bullet.render(surf)
        #draw player on screen:
        surf.blit(self.image, self.rect)
        

        
    
def hangmanimage():

    #load hangman image
    image = pg.image.load('enemy.png').convert()

    #rotate image (delete when new image found)
    #transformed_image = pg.transform.rotate(image, 180)

    #scale our image
    image2 = pg.transform.scale(image, (100,100))

    #create mask. we use this mask to sense collision between bullet and player or alien.
    mask = pg.mask.from_surface(image2)

    #return correct image and mask
    return (image2, mask)
        
def spawn_program_and_die(program, exit_code=0):
    subprocess.Popen(program)
    sys.exit(exit_code)
    
#set screen size:
screen = pg.display.set_mode((1280,720))

#find screen rect:
screen_rect = screen.get_rect()

#add player:
player = Player(screen_rect)

#add killer hangman:
HangmanImage = hangmanimage()

#create an array for hangman so we can kill it:
hangmanarr = []

#set hangman start place:
y = random.randint(-500, -100)
x = random.randint(0, screen_rect.width)

#create hangman
hangmanarr.append(KillerHangman(HangmanImage, (x,y)))

clock = pg.time.Clock()
done = False


while not done:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        player.get_event(event)
    #set screen color:    
    screen.fill((0,0,0))
    delta_time = clock.tick(60)/1000.0
    player.update(keys, delta_time, hangmanarr)
    for e in hangmanarr[:]:
        e.update(delta_time, player)
        #remove hangman when he's dead:
        if e.dead:
            hangmanarr.remove(e)
            def spawn_program_and_die(program, exit_code=0):
                        subprocess.Popen(program)
                        sys.exit(exit_code)
            spawn_program_and_die(['pythonw', 'winscreen.py'])
            pygame.quit()
            sys.exit()
        e.draw(screen)
    player.draw(screen)
    pg.display.update()
    
    
    


# In[ ]:





# In[ ]:




