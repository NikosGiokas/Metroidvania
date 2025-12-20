import pygame
from pygame.locals import *
from sys import exit

# Initialize Pygame
pygame.init()
screenWidth = 1600
screenHeight = 1000
# Set up the game window
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Metroidvania")

class Player:
    x = 0
    y = 0
    health = 5
    velocity = 0
    leftMovement = 0
    rightMovement = 0
    standing = False
    jumping = False
    height = 100
    width = 100

DV = 0.5
GRAVITY = 9.81 / 500
running = True

def give_movement(player: Player, event: pygame.Event):
    if event.type == KEYDOWN:  
        if event.key == K_a:  
            player.leftMovement = DV 
        if event.key == K_d:  
            player.rightMovement = DV  
        if event.key == K_SPACE and player.standing == True:
            player.jumping = True
    if event.type == KEYUP:
        if event.key == K_a:
            player.leftMovement = 0
        if event.key == K_d:  
            player.rightMovement = 0
        if event.key == K_SPACE:
            player.jumping = False

def limit_out_of_bounds(player: Player):
    if player.x < 0: 
        player.x = 1
    elif player.x > screenWidth-player.width:
        player.x = screenWidth-player.width 
    elif player.y < 0:
        player.y = 0 
    elif player.y > screenHeight-player.height:
        player.y = screenHeight-player.height

def apply_vertical_movement(player: Player):
    height_offset = 5
    jump_velocity = -3
    if player.y >= screenHeight-player.height-height_offset and player.y <= screenHeight-player.height+height_offset:
        player.standing = True
    else:
        player.standing = False

    if player.standing == False:
        player.velocity += GRAVITY
    elif player.standing == True:
        player.velocity = 0
    if player.jumping == True and player.standing == True:
        player.velocity = jump_velocity
    player.y += player.velocity

def apply_horizontal_movement(player: Player):
    player.x -= player.leftMovement
    player.x += player.rightMovement

# Game loop 

player = Player()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        give_movement(player, event)
    limit_out_of_bounds(player)
    apply_vertical_movement(player)
    apply_horizontal_movement(player)
    
    screen.fill((30,200,50))
    pygame.draw.rect(screen,(255,0,0),[player.x,player.y,player.width,player.height],0)
    pygame.display.update()

# Quit Pygame
pygame.quit()