import pygame
from spaceinvaders import SpaceInvaders

#Initializing Pygame
pygame.init()

#Initlaizing Game
game = SpaceInvaders()
game.game_loop()






































'''
#Initializing Player
player = Player(game)

#Initliizing Enemy
enemies = []
numEnemies = 4
for i in range(numEnemies):
    enemies.append(Enemy(game))

#Intilaizing Bullet
bullet = Bullet(game)

#Intializing Scoreboard
score = Scoreboard()

#Game loop
running = True
while running:
    #Assigning a fill for the display
    screen.fill((255,255,255))
    
    #Adding Background
    screen.blit(background,(0,0))
    #Tracking User Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        #Shooting/Moving the image based on user input
        elif event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_a: player.xChange = -2
            elif event.key == pygame.K_d: player.xChange = 2
            elif event.key == pygame.K_SPACE: 
                bullet.fireBullet()
                shootingSound.play()
        elif event.type == pygame.KEYUP:
            if   event.key == pygame.K_a: player.xChange += 2
            elif event.key == pygame.K_d: player.xChange -= 2
    
    player.xPos += player.xChange
    for i in range(numEnemies): enemies[i].xPos += enemies[i].xChange

    #Checking Player Boundary
    player.checkBoundary()

    #Checking Enemy Boundary
    for i in range(numEnemies):
        enemies[i].checkBoundary()
        #Checks if enemy has reached the player
        if enemies[i].reachPlayer(player):
            for i in range(numEnemies): enemies[i].hideEnemy()
            game.gameOver(score.score)
    
        
    
    #Bullet Mechanics
    if bullet.isFired == True: 
        bullet.updateBulletPos()
        bullet.drawBullet()
        #Collision Detection
        bullet.isHit(enemies,score)
        bullet.checkBoundary()    
    
    #Update the positions and the display
    player.drawPlayer()
    for i in range(numEnemies): enemies[i].drawEnemy()
    score.showScore()
    pygame.display.update()
    '''