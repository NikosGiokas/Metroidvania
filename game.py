import pygame
from pygame.locals import *
from sys import exit
import json

# Initialize Pygame
pygame.init()
screenWidth = 1600
screenHeight = 1000
# Set up the game window
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Metroidvania")

DV = 0.5
GRAVITY = 9.81 / 450
running = True
seed = "000019150902120902120902120712021102110411051109021204110612190316071100"

class Size:
    width = 0
    height = 0
    def __init__(self,width,height):
        self.width = width
        self.height = height
    
class Point:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = round(x)
        self.y = round(y)

class Player:
    location = Point(450,250)
    health = 5
    velocity = 0
    leftMovement = 0
    rightMovement = 0
    jumping = False
    size = Size(80,80)
    def is_jumping(self):
        return self.velocity < 0
    def can_jump(self):
        return not self.is_jumping() and is_colliding_top(blocks, self.location, self.size, self.velocity)

class Block:
    x = 0
    y = 0
    size = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def contains(self, point: Point):
        return point.x >= self.x and point.x <= self.x + self.size and point.y >= self.y and  point.y <= self.y + self.size

class Enemy:
    position = Point(0,0)
    health = 1
    speed = 0.2
    rightMovement = 0.2
    leftMovement = -0.2
    velocity = 0
    size = Size(100,100)
    def __init__(self, position: Point):
        self.position = position
    
class Testenemy(Enemy):
    rightMovement = 0.2
    leftMovement = -0.2
    health = 11
    size = Size(50,20)
    def do_vertical_movement(self, blocks: list[Block]):
        if not is_colliding_top(blocks, self.position, self.size, self.velocity+1):
            self.velocity += GRAVITY
        else:
            self.velocity = 0
        self.position.y += self.velocity
        
    def do_horizontal_movement(self, blocks: list[Block]):
        if is_colliding_left(blocks, self.position, self.size, self.rightMovement):
            print("is_colliding_left")
            self.speed = self.leftMovement
        elif is_colliding_right(blocks, self.position, self.size, self.leftMovement):
            print("is_colliding_right")
            self.speed = self.rightMovement
        # if not is_fully_colliding_top(blocks, self.position, self.size, self.velocity):
        #     print("not is_fully_colliding_top")
        #     self.speed *= -1
        self.position.x += self.speed

def check_collisions(point1: Point, width1: int, height1: int, point2: Point, width2: int, height2: int):
    return point1.x + width1 >= point2.x and point1.x <= point2.x + width2 and point1.y + height1 >= point2.y and point1.y <= point2.y + height2

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
    if player.location.x < 0: 
        player.location.x = 1
    elif player.location.x > screenWidth-player.size.width:
        player.location.x = screenWidth-player.size.width 
    elif player.location.y < 0:
        player.location.y = 0 
    elif player.location.y > screenHeight-player.size.height:
        player.location.y = screenHeight-player.size.height

def apply_gravity(player: Player):
    jump_velocity = -3
    if not is_colliding_top(blocks,player.location,player.size,player.velocity):
        player.velocity += GRAVITY
    else:
        player.velocity = 0
    if player.jumping == True:
          if player.can_jump():
            player.velocity = jump_velocity
    


def apply_horizontal_movement(player: Player):
    player.location.x -= player.leftMovement
    player.location.x += player.rightMovement
# Returns the room number
def room_number(seed: str):
    return seed[:3]
# Returns the map relevant 
def room_map(seed: str):
    return seed[4:]
               
def create_enemies_from_seed(seed: str):
    enemyArray: list = []
    newX = 50
    newY = 50
    for i in range(len(seed)-1):
        if seed[i] == "2": 
            i += 1
            for j in range(int(seed[i])):
                enemyArray.append(Testenemy(Point(newX, newY)))
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
        elif seed[i] == "1":
            i += 1
            for j in range(int(seed[i])):
                if newX > screenWidth - 200:
                    newX = 50
                    newY += 100
                else: 
                    newX += 100
        i += 1
    return enemyArray
               
def draw_blocks(blocks: list[Block]):
    for i in range(len(blocks)):
        pygame.draw.rect(screen,(0,255,0),[blocks[i].x,blocks[i].y,blocks[i].size,blocks[i].size],0)

def is_colliding_top(blocks: list[Block], location: Point, size: Size, velocity):
    for block in blocks:
        left_bottom_player_part = Point(location.x, location.y + size.height + velocity)
        right_bottom_player_part = Point(location.x + size.width, location.y + size.height + velocity)
        if block.contains(left_bottom_player_part) or block.contains(right_bottom_player_part):
            return True
    return False

def is_fully_colliding_top(blocks: list[Block], location: Point, size: Size, velocity):
    for block in blocks:
        left_bottom_player_part = Point(location.x, location.y + size.height + velocity)
        right_bottom_player_part = Point(location.x + size.width, location.y + size.height + velocity)
        if block.contains(left_bottom_player_part) and block.contains(right_bottom_player_part):
            return True
    return False

def is_colliding_bottom(blocks: list[Block], player: Player):
    for block in blocks:
        left_top_player_part = Point(player.location.x, player.location.y + player.velocity)
        right_top_player_part = Point(player.location.x + player.size.width, player.location.y + player.velocity)
        if block.contains(left_top_player_part) or block.contains(right_top_player_part):
            return True
    return False

def is_colliding_left(blocks: list[Block], location: Point, size: Size, rightMovement):
    for block in blocks:
        right_top_player_part = Point(location.x + size.width + rightMovement, location.y)
        right_bottom_player_part = Point(location.x + size.width + rightMovement, location.y + size.height)
        if block.contains(right_top_player_part) or block.contains(right_bottom_player_part):
            return True
    return False

def is_colliding_right(blocks: list[Block], location: Point, size: Size, leftMovement):
    for block in blocks:
        left_top_player_part = Point(location.x - leftMovement, location.y)
        left_bottom_player_part = Point(location.x - leftMovement, location.y + size.height)
        if block.contains(left_top_player_part) or block.contains(left_bottom_player_part):
            return True
    return False

def do_block_collisions(blockArray: list[Block], player: Player):
    if is_colliding_top(blockArray, player.location, player.size, player.velocity):
        player.velocity = 0
    if is_colliding_left(blockArray, player.location, player.size, player.rightMovement):
        player.location.x -= player.rightMovement
    if is_colliding_right(blockArray, player.location, player.size, player.leftMovement):
        player.location.x += player.leftMovement
    if is_colliding_bottom(blockArray, player):
        player.velocity = 0
        
def do_enemy_movement(enemyArray: list[Enemy],blockArray: list[Block]):
    for enemy in enemyArray:
        enemy.do_vertical_movement(blockArray)
        enemy.do_horizontal_movement(blockArray)
        
def draw_player(player: Player):
    pygame.draw.rect(screen,(255,0,0),[player.location.x,player.location.y,player.size.width,player.size.height], 0)
        
def draw_borders():
    pygame.draw.rect(screen,(0,0,0),[0,0,screenWidth,50],0)
    pygame.draw.rect(screen,(0,0,0),[0,0,50,screenHeight],0)
    pygame.draw.rect(screen,(0,0,0),[0,screenHeight - 50,screenWidth,50],0)
    pygame.draw.rect(screen,(0,0,0),[screenWidth - 50,0,50,screenHeight],0)
    
def draw_health(player: Player):
    for i in range(player.health):
        pygame.draw.rect(screen,(255,0,0),[44*i+50,5,40,40],0)

def draw_enemies(enemies: list[Enemy]):
    for enemy in enemies:
        pygame.draw.rect(screen,(0,255,255),[enemy.position.x,enemy.position.y,enemy.size.width,enemy.size.height], 0)

# Game loop 
player = Player()

def get_blocks():
    with open('level_01.json', 'r') as file:
        data = json.load(file)

    blocks: list[Block] = []
    for block_data in data["blocks"]:
        blocks.append(Block(block_data["x"], block_data["y"]))
    return blocks

def get_enemies():
    with open('level_01.json', 'r') as file:
        data = json.load(file)

    enemies: list[Enemy] = []
    for enemy_data in data["enemies"]:
        enemies.append(Testenemy(Point(enemy_data["x"], enemy_data["y"])))
    return enemies

blocks = get_blocks()
enemies = get_enemies()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        give_movement(player, event)
    apply_gravity(player)
    limit_out_of_bounds(player)
    do_block_collisions(blocks, player)
    #apply_vertical_movement(player, blocks)
    player.location.y += player.velocity
    apply_horizontal_movement(player)
    
    do_enemy_movement(enemies, blocks)
    
    
    screen.fill((30,200,50))
    draw_blocks(blocks)
    draw_enemies(enemies)
    draw_player(player)
    draw_borders()
    draw_health(player)
    pygame.display.update()

# Quit Pygame
pygame.quit()