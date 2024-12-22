import pygame
import time
import random
pygame.font.init()  #initialise font mondule

WIDTH , HEIGHT = 1000 , 700                      #window dimensions in pixels
WIN = pygame.display.set_mode((WIDTH, HEIGHT))   #window declaration
pygame.display.set_caption("Space Dodge")        #Window Title

BG = pygame.transform.scale(pygame.image.load("space_image.png"),(WIDTH,HEIGHT))     #Set the background image
     #Scale the image to fill the window

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT =pygame.font.SysFont("comicsans", 30)
                          #font name   #font size

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0,0))    #Project background image to screen

    time_text =FONT.render(f"Time: {round(elapsed_time)}s",1, "white")
                #text that we want to render           #second  #1:anti-aliasing      
    WIN.blit(time_text,(10,10))

    pygame.draw.rect(WIN, "red" , player)  #Drawing the player character
    
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update() #Refresh display image 




def main():    #Main game logic e.g movement, events...
    run = True


    player = pygame.Rect(200 , HEIGHT - PLAYER_HEIGHT , PLAYER_WIDTH , PLAYER_HEIGHT)  #our player character
                        #player location/position       #player dimensions
    
    clock = pygame.time.Clock() #Regulates the speed of our loop/character

    start_time = time.time()  #get the current time when the game started
    elapsed_time =0

    star_add_increment =2000   #first projectile at 2000ms
    star_count = 0             #when to add another projectile

    stars=[]
    hit =False

    while run:            #Continue showing the window

        #counting how many ms since last clock tick
        star_count += clock.tick(60) #Run at a maximum rate of 60 times per second
        elapsed_time = time.time() - start_time  

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0,WIDTH - STAR_WIDTH)   #pick random location for projectile
                star =pygame.Rect(star_x , -STAR_HEIGHT , STAR_WIDTH,STAR_HEIGHT)  #-star_height since projectile must be seen entering the window
                stars.append(star)  #append a projectile to the list

            star_add_increment =max(200, star_add_increment-50)  #decreasing the time to add a projectile
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed() #get the keys that the user has pressed
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL>= 0:  #Left arrow key pressed
                                   #Adding player boundary so player does not move off window
            player.x -= PLAYER_VEL
        

        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:  #Right arrow key pressed
            player.x += PLAYER_VEL
        
                         #make a copy of list stars so that projectiles which have reached bottom are removed
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)  #remove projectile when bottom reached or collide with player
                hit = True
                break
        if hit:
            lost_text = FONT.render("Game Over", 1, "white")
            WIN.blit(lost_text, (WIDTH/2-lost_text.get_width()/2, HEIGHT/2 -lost_text.get_height()/2))
            #Write text in the middle of the screen

            pygame.display.update()  #update window
            pygame.time.delay(4000)  #freeze game to see text
            break  #quit game

        draw(player, elapsed_time,stars)   #Background image

    pygame.quit()

if __name__ == "__main__":
    main()