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
    x = 250
    y = 250
    health = 5
    velocity = 0
    leftMovement = 0
    rightMovement = 0
    standing = False
    jumping = False
    height = 80
    width = 80

class Point:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = round(x)
        self.y = round(y)

class Block:
    x = 0
    y = 0
    size = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def contains(self, point: Point):
        return point.x >= self.x and point.x <= self.x + self.size and point.y >= self.y and  point.y <= self.y + self.size

DV = 0.5
GRAVITY = 9.81 / 450
running = True
blockArray = []
seed = "000019150902120902120902120712021102110411051109021204110612190316071100"



def give_movement(player: Player, event: pygame.Event):
    if event.type == KEYDOWN:  
        if event.key == K_a:  
            player.leftMovement = DV 
        if event.key == K_d:  
            player.rightMovement = DV  
        if event.key == K_SPACE :
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

def apply_gravity(player: Player):
    jump_velocity = -3
    if player.standing == False:
        player.velocity += GRAVITY
    elif player.standing == True:
        player.velocity = 0
    if player.jumping == True and player.standing == True:
        player.velocity = jump_velocity

def apply_vertical_movement(player: Player, blocks: list[Block]):
    height_offset = 5    
    is_on_bottom = player.y >= screenHeight-player.height and player.y <= screenHeight-player.height
        
    if is_on_bottom or is_on_top(blocks, player):
        player.standing = True
    else:
        player.standing = False
    player.y += player.velocity

def apply_horizontal_movement(player: Player):
    player.x -= player.leftMovement
    player.x += player.rightMovement

# Returns the room number
def room_number(seed: str):
    return seed[:3]

# Returns the map relevant 
def room_map(seed: str):
    return seed[4:]

def create_blocks_from_seed(seed: str):
    blockArray: list = []
    genNum = 0
    newX = 50
    newY = 50
    for i in range(len(seed)-1):
        if seed[i] == "1": 
            i += 1
            for j in range(int(seed[i])):
                blockArray.append(Block(newX, newY))
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
               
def draw_blocks(blocks: list[Block]):
    for i in range(len(blocks)):
        pygame.draw.rect(screen,(0,255,0),[blocks[i].x,blocks[i].y,blocks[i].size,blocks[i].size],0)

def is_on_top(blocks: list[Block], player: Player):
    top_offset = 1
    for block in blocks:
        left_bottom_player_part = Point(player.x, player.y + player.height + top_offset)
        right_bottom_player_part = Point(player.x + player.width, player.y + player.height + top_offset)
        if block.contains(left_bottom_player_part) or block.contains(right_bottom_player_part):
            return True
    return False

def is_colliding_top(blocks: list[Block], player: Player):
    for block in blocks:
        left_bottom_player_part = Point(player.x, player.y + player.height + player.velocity)
        right_bottom_player_part = Point(player.x + player.width, player.y + player.height + player.velocity)
        if block.contains(left_bottom_player_part) or block.contains(right_bottom_player_part):
            return True
    return False

def is_colliding_bottom(blocks: list[Block], player: Player):
    for block in blocks:
        left_top_player_part = Point(player.x, player.y + player.velocity)
        right_top_player_part = Point(player.x + player.width, player.y + player.velocity)
        if block.contains(left_top_player_part) or block.contains(right_top_player_part):
            return True
    return False

def is_colliding_left(blocks: list[Block], player: Player):
    for block in blocks:
        right_top_player_part = Point(player.x + player.width + player.rightMovement, player.y)
        right_bottom_player_part = Point(player.x + player.width + player.rightMovement, player.y + player.height)
        if block.contains(right_top_player_part) or block.contains(right_bottom_player_part):
            return True
    return False

def is_colliding_right(blocks: list[Block], player: Player):
    for block in blocks:
        left_top_player_part = Point(player.x - player.leftMovement, player.y)
        left_bottom_player_part = Point(player.x - player.leftMovement, player.y + player.height)
        if block.contains(left_top_player_part) or block.contains(left_bottom_player_part):
            return True
    return False

def do_block_collisions(blockArray: list[Block], player: Player):
    if is_colliding_top(blockArray, player):
        player.velocity = 0
        player.standing = True
    if is_colliding_left(blockArray, player):
        player.x -= player.rightMovement
    if is_colliding_right(blockArray, player):
        player.x += player.leftMovement
    if is_colliding_bottom(blockArray, player):
        player.velocity = 0

# Game loop 
blocks = create_blocks_from_seed(room_map(seed))
player = Player()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        give_movement(player, event)
    apply_gravity(player)
    limit_out_of_bounds(player)
    do_block_collisions(blocks, player)
    apply_vertical_movement(player, blocks)
    apply_horizontal_movement(player)
    
    screen.fill((30,200,50))
    draw_blocks(blocks)
    pygame.draw.rect(screen,(255,0,0),[player.x,player.y,player.width,player.height],0)
    pygame.display.update()

# Quit Pygame
pygame.quit()