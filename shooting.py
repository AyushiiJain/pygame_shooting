  
    
#IMPORT PYGAME AND INITIALIZATION OF PYGAME
import pygame
import random
import math
from pygame import mixer

pygame.init()

#decide width and height of the window
screen_height=600
screen_width=800

#make the game window
screen=pygame.display.set_mode((screen_width,screen_height))

#background
background = pygame.image.load('background.png')

#backg sound
mixer.music.load('background.wav')
mixer.music.play(-1)  #for continuous sound of backg.

#change title and icon
pygame.display.set_caption("GAME WARS")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)



#player
player_img = pygame.image.load('spaceship1.png')
playerX = 370
playerY = 480 
playerX_change = 0


#enemy
#for multiple enemy create list
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):    
     enemy_img.append(pygame.image.load('virus.png'))
     enemy_img.append(pygame.image.load('virus2.png'))
     enemyX.append(random.randint(0,736))
     enemyY.append(random.randint(50,150))
     enemyX_change.append(3)
     enemyY_change.append(40)

#bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 7.2
bullet_state= "ready"
# ready - u cant see the bullet on the screen
# fire - the bullet is currently moving

#score 

score_value = 0
font = pygame.font.Font('Yellow Rabbit - Personal Use.otf',32)

textX = 10
textY = 10

#game over text
game_over_font = pygame.font.Font('Yellow Rabbit - Personal Use.otf',64)


def show_score(x,y):
     score = font.render("Score: " + str(score_value),True,(255,255,255))
     screen.blit(score,(x,y))

def game_over_text():
     game_over_text = game_over_font.render(" GAME OVER! ",True,(255,255,255))
     screen.blit(game_over_text,(250,250))
      
def player(x,y):
    #to draw player's image onto screen use .blit(), req 2 paramters
    screen.blit(player_img,(x,y))

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state= "fire"
    screen.blit(bullet_img,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2))
    if distance < 27:  #dist btw enemy and collison=27
        return True
    else:
        return False
    

#game loop
running = True 
#ensures a continuous loop keeps the game running
while running:
    screen.fill((0,0,0))

    #background image
    screen.blit(background,(0,0))
   
    #RGB
    #tracks avery event while the game is running
    for event in pygame.event.get():
        #checks if user pressed "quit" button of screen
        if event.type==pygame.QUIT:
            #sets running to false
            running=False
   
        #check if key was pressed and whether left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 3.4
            if event.key == pygame.K_SPACE:
                #only press spacebar when in ready condition
                if bullet_state is "ready":
                     bullet_Sound = mixer.Sound('laser.wav')
                     bullet_Sound.play()  #sound for shorter interval of bullet
                     #get current x coord of spaceship
                     bulletX = playerX
                     fire_bullet(bulletX,bulletY)
                  
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                #set change in coordinate to 0 to make it stop moving

    #checking for boundaries so that it does not go out of bounds
    playerX +=playerX_change

    if playerX <=0:
        playerX =0
        #take into account the image size of player
    elif playerX >= 736:
        playerX = 736
        
    # Enemy movement
    
    for i in range(num_of_enemies):

         #game over
         if enemyY[i] > 465:
              for j in range(num_of_enemies):
                   enemyY[j] = 2000
              game_over_text()
              break
          
         enemyX[i] += enemyX_change[i]
         if enemyX[i] <=0:
              enemyX_change[i] =3
              enemyY[i] += enemyY_change[i]
              #take into account the image size of player
         elif enemyX[i] >= 736:
              enemyX_change[i] = -3
              enemyY[i] += enemyY_change[i]

         #collsion(not to put inside elif or if condition. Only 'for' loop
         collision= isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
         if collision:
             explosion_Sound = mixer.Sound('explosion.wav')
             explosion_Sound.play()
             bulletY=480
             bullet_state= "ready"
             score_value += 1    
         
             enemyX[i] = random.randint(0,736)
             enemyY[i] = random.randint(50,150)
         
         enemy(enemyX[i],enemyY[i],i)
         

    #bullet movement
    if bulletY <=0:
        bulletY=480
        bullet_state="ready"
        
    
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-= bulletY_change


    player(playerX,playerY)
    show_score(textX,textY)
    
    pygame.display.update()
#closes the game window
pygame.quit()



#enter name and highest score
#restart
#multiple bullet
