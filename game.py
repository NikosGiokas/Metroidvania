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
    height = 80
    width = 80

class Block:
    x = 0
    y = 0
    size = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y



DV = 0.5
GRAVITY = 9.81 / 450
running = True
blockArray = []
seed = "000019150902120902120902120712021102110411051109021204110612191316071100"



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

# Returns the room number
def room_number(seed):
    return seed[:3]

# Returns the map relevant 
def room_map(seed):
    return seed[4:]

def create_blocks_from_seed(seed: str):
    blockArray: list = []
    genNum = 0
    newX = 50
    newY = 50
#    if seed[2] == "0" and seed[3] == "0" and seed[4] != "0":
#        print("went")
#        genNum = 4
    for i in range(len(seed)-1):
        if seed[i] == "1": 
            i += 1
            for j in range(int(seed[i])):
                blockArray.append(Block(newX,newY))
                if newX > screenWidth - 200:
                    newX = 50
                    newY += 100
                else:
                    newX += 100
        elif seed[i] == "0":
            i += 1
            for j in range(int(seed[i])):
                if newX > screenWidth - 200:
                    newX = 50
                    newY += 100
                else: 
                    newX += 100
        i += 1
    return blockArray
           
def draw_blocks(blockArray: list):
    for i in range(len(blockArray)):
        pygame.draw.rect(screen,(0,255,0),[blockArray[i].x,blockArray[i].y,blockArray[i].size,blockArray[i].size],0)



# Game loop 
blocks = create_blocks_from_seed(room_map(seed))
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
    draw_blocks(blocks)
    pygame.draw.rect(screen,(255,0,0),[player.x,player.y,player.width,player.height],0)
    pygame.display.update()

# Quit Pygame
pygame.quit()