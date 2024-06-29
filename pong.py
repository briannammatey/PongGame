import pygame
from pygame.locals import *
import random



#initializing the code
pygame.init()

#screen dimensions
WIDTH=800
HEIGHT=600

running=True
paused =True

#if game is not paused update both players
if not paused:
    player1.y += player1.move*timeSec
    player2.y+= player2.move*timeSec
    ball.x+= ball.xMove*timeSec
    ball.y+= ball.yMove*timeSec

#creates clock Object
clock =pygame.time.Clock()

#initializes a font object
font = pygame.font.SysFont("calibri", 40)

##creates a game window
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Pong")

#sets up backgroud
back=pygame.Surface((WIDTH, HEIGHT))
background=back.convert()
background.fill((0,0,0))

#defines player atributes, speed, movement, score, dimensions, and image
class Player():
    x=0
    y=0
    speed=250.0
    move=0
    score=0
    height=76
    width=10
    image=pygame.Surface((width, height)).convert()
    image.fill((0,0,255))

#defines ball atributes, speed, movement, score dimensions ad image
class Ball():
    size=16
    x=WIDTH/2-size/2
    y=HEIGHT/2-size/2
    xMove=250
    yMove= 250
    image = pygame.Surface((size,size))
    pygame.draw.circle(image, (0,255,0), (int(size/2), int(size/2)), int(size/2))
    image= image.convert()
    
##player and ball initialization 
player1= Player()
player2=Player()
ball=Ball()


player1.x=10
player1.y= HEIGHT/2-player1.height/2

player2.x=WIDTH - 10 - player2.width

player2.y= HEIGHT/2 - player2.height/2
    



"""
event handeling Handles QUIT to exit the game,
KEYDOWN to move players 1 and 2 up and down
KEYUP, stop the player movement and pause the game
KEY_SPACE to pause the game
"""
while running:
    
    for event in pygame.event.get():
        if event.type==QUIT:
            running = False
        elif event.type==KEYDOWN:

            ##handle key pressed events
            if event.key==K_w:
                player1.move=-player1.speed
            elif event.key==K_s:
                player1.move=player1.speed
            elif event.key==K_UP:
                player2.move=-player2.speed
            elif event.key ==K_DOWN:
                player2.move=player2.speed
            elif paused and event.key==K_SPACE:
                paused=False

        elif event.type==KEYUP:
            ##handles key released events
            paused=False
            if event.key ==K_w or event.key == K_s:
                player1.move=0
            elif event.key== K_UP or event.key==K_DOWN:
                player2.move=0
        
    """
    Game Logic: Updates player and ball positions based on time passed (timePassed),
    handles collisions with screen boundaries and players,
    updates scores, and resets the ball position when a goal is scored.
    """
    timePassed=clock.tick(30)
    timeSec=timePassed/1000.0
    ##move
    player1.y+=player1.move *timeSec
    player2.y += player2.move*timeSec
    ball.x+=ball.xMove*timeSec
    ball.y+=ball.yMove*timeSec

    #ensures players stay within screen boundaries
    if player1.y>=HEIGHT - player1.height-10:
        player1.y=HEIGHT-player1.height-10
    elif player1.y<=10:
        player1.y=10
    if player2.y>= HEIGHT - player2.height-10:
        player2.y=HEIGHT - player2.height -10
    elif player2.y<=10:
        player2.y=10

   #ensures the ball stays within screen boundaries
    if ball.y<=10.0:
        ball.yMove=-ball.yMove
        ball.y=10.0
    elif ball.y>=HEIGHT-10- ball.size:
        ball.yMove= -ball.yMove
        ball.y=HEIGHT-10-ball.size

    #ball does not collide with players
    if ball.x<=player1.x + player1.width:
        if ball.y +ball.size>=player1.y and ball.y <= player1.y+ player1.height:
            ball.x=player1.x + player1.width +5
            ball.xMove= -ball.xMove

    if ball.x+ ball.size>= player2.x:
        if ball.y+ball.size>= player2.y and ball.y<= player2.y +player2.height:
            ball.x= player2.x- player2.width-5
            ball.xMove=-ball.xMove

    ##scroring logic
    if ball.x<5.0:
        player2.score+=1
    elif ball.x>WIDTH-5-ball.size:
        player1.score+=1

    #reset ball if scoring occurs
    if ball.x < 5.0 or ball.x> WIDTH-5-ball.size:
        ball.x=WIDTH/2 -ball.size/2
        ball.y= HEIGHT/2 -ball.size/2
        player1.y= HEIGHT/2-player1.height/2
        player2.y= HEIGHT/2-player2.height/2
        paused =True
        
    
    
                
                
            
    """
    Rendering: Clears the screen with screen.blit(background, (0, 0)),
    draws a center line with pygame.draw.aaline(),
    blits player1, player2, ball, and their scores (score1, score2) onto the screen,
    and displays a message if the game is paused (paused).

    """
    screen.blit(background, (0,0))
    pygame.draw.aaline(screen, (255, 255, 255), (int(WIDTH/2),5), ((int(WIDTH/2),HEIGHT-5))) 
    
    screen.blit(player1.image, (player1.x, player1.y))
    screen.blit(player1.image, (player2.x, player2.y))
    screen.blit(ball.image, (ball.x, ball.y))

    score1=font.render(str(player1.score), True, (255, 255, 255))
    score2=font.render(str(player2.score), True, (255, 255, 255))
    screen.blit(score1, (15, 15))
    screen.blit(score2, (WIDTH/2+15,15))

    if(paused):
        screen.blit(font.render("Press SPACE to start round", True,(255, 255, 255)), (WIDTH/2 - 210, HEIGHT/2-70 ) ) 
    pygame.display.update()

#close the game        
pygame.quit()

