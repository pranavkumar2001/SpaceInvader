# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 19:44:11 2021

@author: Pranav Kumar
"""
#importing modules
import pygame
import random
import math
import os

pygame.init()
from pygame import mixer

#player
playerimg=pygame.image.load("spaceship.png")
playerimg=pygame.transform.scale(playerimg,(100,100))
player_x=350
player_y=500
player_x_change=0
player_y_change=0

#enemy
enemyimg=[]
enemy_x=[]
enemy_y=[]
enemy_x_change=[]
enemy_y_change=[]
enemypic=pygame.image.load("enemy.png")
enemypic=pygame.transform.scale(enemypic,(64,64))
for i in range(6):
    enemyimg.append(enemypic)
    enemy_x.append(random.randint(0,700))
    enemy_y.append(random.randint(15,150))
    enemy_x_change.append(3)
    enemy_y_change.append(40)

#bullet
bulletimg=pygame.image.load("bullet.png")
bulletimg=pygame.transform.scale(bulletimg,(18,18))
bullet_x=0
bullet_y=470
bullet_x_change=0.4
bullet_y_change=5
bullet_state="ready" #ready=bullet is not visible

#icon
icon=pygame.image.load("spaceship.png")
icon=pygame.transform.scale(icon,(64,64))

#backgroung image
backimg=pygame.image.load("background.jpg")
backimg=pygame.transform.scale(backimg,(800,600))

#creating game window
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption("Pranav's Space Invaders")
pygame.display.set_icon(icon)
pygame.display.update()
 
#game variables
score=0
no_enemy=6
running=True
font=pygame.font.SysFont(None,30)

#Opening highscore file    
if(not os.path.exists("maxscore.txt")):
     with open("maxscore.txt","w") as f:
            f.write("0")
with open("maxscore.txt","r") as f:
    highscore=f.read()
    
#functions
def show_text(text,x,y):
    text=font.render(text,True,(255,255,255))
    screen.blit(text,(x,y))

def player(x,y):
    screen.blit(playerimg,(player_x,player_y))
    
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))    
    
def firebullet(x,y):
    global bullet_state
    bullet_state="fire" #fire means bullet is visible
    screen.blit(bulletimg,(x+38,y))
    
def isCollision(enemy_x,enemy_y,bullet_x,bullet_y):
    distance=math.sqrt(math.pow(enemy_x-bullet_x,2)+math.pow(enemy_y-bullet_y,2))
    if distance<=40:
        return True
    else:
        return False
    
def gameover():
    player_x=2000
    for j in range(6):
        enemy_y[j]=2000   
    screen.blit(backimg,(0,0))   
    show_text("SCORE:"+str(score),300,160)
    show_text("GAME OVER",300,200)
    with open("maxscore.txt","w") as f:
         f.write(str(highscore))     
    
 

#Game Loop
def gameloop():
    #assigning global variables
    global running 
    global score
    global player_x
    global player_y
    global player_x_change
    global player_y_change
    global bullet_x
    global bullet_y
    global bullet_state
    global highscore
    global enemy_x
    global enemy_y
    global enemy_x_change
    global enemy_y_change
    down=True
    mixer.music.load('blazersong.wav')    
    mixer.music.play(-1)  
    while running:
        screen.blit(backimg,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    player_x_change-=0.7
                if event.key==pygame.K_RIGHT:
                    player_x_change+=0.7 
                if event.key==pygame.K_SPACE:
                    bullet_state="fire" 
                    bullet_x=player_x
                if event.key==pygame.K_q: #cheat code
                    highscore+=1000
                   
                   
            if event.type==pygame.KEYUP:
                player_x_change=0
              
        player_x+=player_x_change       
        if  player_x<0:
            player_x=0
        if player_x>=700:
            player_x=700
            
        for i in range(6):
            enemy_x[i]+=enemy_x_change[i]
            
            if  enemy_x[i]<0:
                enemy_x_change[i]=0.5
                enemy_y[i]+=enemy_y_change[i]
            if enemy_x[i]>=700:
                enemy_x_change[i]=-0.5
                enemy_y[i]+=enemy_y_change[i]
                
            collision=isCollision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)    
        
            if collision:
                sound=mixer.Sound('shot.mp3')
                sound.play()
                bullet_y=480
                #bullet_state="ready"
                score+=1
                if score>int(highscore):
                    highscore=score
                enemy_x[i]=random.randint(0,690)
                enemy_y[i]=random.randint(15,150)     
            
            enemy(enemy_x[i],enemy_y[i],i)
            
        if bullet_y<=0:
            #bullet_state="ready"
            bullet_y=480
           
        bullet_x=player_x
        if bullet_state == "fire":
            firebullet(bullet_x,bullet_y)
            bullet_y-=bullet_y_change             
            
        player(player_x,player_y)   
        show_text("SCORE: "+str(score)+"   HIGHSCORE:"+str(highscore),10,10)
        #Game Over
        show_text("PRANAV KUMAR",630,570)
        #game over
        for e in enemy_y:
            if e>=450:
                gameover()
                break
    
        pygame.display.update()

#main() i.e calling functions    
gameloop()       
pygame.quit()
        