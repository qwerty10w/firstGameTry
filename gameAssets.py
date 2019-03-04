import math
import pygame
from resources import *
pygame.init()
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("First Game")

enemies = pygame.sprite.Group()



class level():
    def loadFile(self, filename="level.map"):
        self.map = []
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.width = len(self.map[0])
        self.height = len(self.map)

    def getTile(self, x ,y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def getBool(self, x, y, name):
        value = self.getTile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    def isWall(self, x, y):
        self.getBool(x, y, "wall")

    def render(self):
        wall = self.isWall()
        tiles = MAP_CACHE[self.tileset]
        image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if wall(map_x, map_y):
                    # Draw different tiles depending on neighbourhood
                    if not wall(map_x, map_y+1):
                        if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                            tile = 1, 2
                        elif wall(map_x+1, map_y):
                            tile = 0, 2
                        elif wall(map_x-1, map_y):
                            tile = 2, 2
                        else:
                            tile = 3, 2
                    else:
                        if wall(map_x+1, map_y+1) and wall(map_x-1, map_y+1):
                            tile = 1, 1
                        elif wall(map_x+1, map_y+1):
                            tile = 0, 1
                        elif wall(map_x-1, map_y+1):
                            tile = 2, 1
                        else:
                            tile = 3, 1
                    # Add overlays if the wall may be obscuring something
                    if not wall(map_x, map_y-1):
                        if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                            over = 1, 0
                        elif wall(map_x+1, map_y):
                            over = 0, 0
                        elif wall(map_x-1, map_y):
                            over = 2, 0
                        else:
                            over = 3, 0
                        overlays[(map_x, map_y)] = tiles[over[0]][over[1]]
                else:
                    try:
                        tile = self.key[c]['tile'].split(',')
                        tile = int(tile[0]), int(tile[1])
                    except (ValueError, KeyError):
                        # Default to ground tile
                        tile = 0, 3
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                           (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
        return image, overlays


class player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 2
        self.left = False
        self.right = False
        self.up = False
        self.down = True
        self.walkCount = 0
        self.standing = True
        self.attacking = False
        self.healthLevel = 5
        self.detected = False
        self.damaged  = False
        self.hitbox = (self.x + 25, self.y, self.width, self.height)
        self.rect = pygame.Rect(self.x + 25, self.y, self.width, self.height)
    def draw(self, window):
        if self.walkCount + 1 > 30:
            self.walkCount = 0
        if not(self.standing):
            if self.left and self.up:
                window.blit(walkUp[self.walkCount//6], (self.x,self.y))
                self.walkCount +=1
            elif self.left and self.down:
                window.blit(walkLeft[self.walkCount//6], (self.x,self.y))
                self.walkCount +=1
            elif self.right and self.up:
                window.blit(walkUp[self.walkCount//6], (self.x,self.y))
                self.walkCount +=1
            elif self.right and self.down:
                window.blit(walkRight[self.walkCount//6], (self.x,self.y))
                self.walkCount +=1
            elif self.left:
                window.blit(walkLeft[self.walkCount//6], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                window.blit(walkRight[self.walkCount//6], (self.x,self.y))
                self.walkCount +=1
            elif self.up:
                window.blit(walkUp[self.walkCount//6], (self.x,self.y))
                self.walkCount +=1
            elif self.down:
                window.blit(walkDown[self.walkCount//6], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.left:
                window.blit(walkLeft[0], (self.x, self.y))
            if self.right:
                window.blit(walkRight[0], (self.x, self.y))
            if self.down:
                window.blit(idle[self.walkCount//6], (self.x,self.y))
                self.walkCount +=1
            if self.up:
                window.blit(pygame.image.load("Assets/Player/knight iso char_idle up_0.png"), (self.x, self.y))
        self.rect = pygame.Rect(self.x + 25, self.y, self.width, self.height)

class enemy(pygame.sprite.Sprite):
    def __init__(self, type, x, y, width, height, vel):
        pygame.sprite.Sprite.__init__(self, enemies)
        self.type = type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.left = False
        self.right = False
        self.up = False
        self.down = True
        self.walkCount = 0
        self.attackCount = 0
        self.standing = True
        self.attacking = False
        self.Dmg = False
        self.healthLevel = 5

    def printType(self):
        print(self.type)

class skeleton(enemy):
    def __init__(self, type, x, y, width, height, vel):
        super().__init__(type, x, y, width, height, vel)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height - 10)
    def draw(self, window):
        if self.type == "Skeleton":
            if self.walkCount + 1 > 36:
                self.walkCount = 0
            if self.attackCount + 1 > 54:
                self.attackCount = 0
                self.attacking = False
                self.left = False
                self.right = False
                self.Dmg = False
                man.damaged  = False

            if self.attacking and self.right:
                window.blit(pygame.transform.scale2x(skelAttack[self.attackCount//3]), (self.x, self.y - 9))
                self.attackCount += 1
                if self.attackCount >= 24 and self.attackCount <= 33:
#                    pygame.draw.rect(window, (255,255,255), (self.x + 15, self.y, self.width, self.height), 1) #hitbox
                    self.Dmg = True


            elif self.attacking and self.left:
                window.blit(pygame.transform.scale2x(pygame.transform.flip(skelAttack[self.attackCount//3], True, False)), (self.x - 40, self.y - 9))
                self.attackCount += 1
                if self.attackCount >= 24 and self.attackCount <= 33:
#                    pygame.draw.rect(window, (255,255,255), (self.x - 35, self.y, self.width, self.height), 1) #hitbox
                    self.Dmg = True

            if not(self.standing) and not(self.attacking):
                if self.left:
                    window.blit(pygame.transform.scale2x(pygame.transform.flip(skelWalkRight[self.walkCount//3], True, False)), (self.x,self.y))
                    self.walkCount += 1
                if self.right:
                    window.blit(pygame.transform.scale2x(skelWalkRight[self.walkCount//3]), (self.x,self.y))
                    self.walkCount += 1
            elif self.standing:
                window.blit(pygame.transform.scale2x(skelIdle[self.walkCount//4]), (self.x,self.y))
                self.walkCount += 1
    def move(self):
        if (math.sqrt(pow((man.x - self.x), 2) + pow((man.y - self.y), 2)) <= 425):
            self.standing = False
            man.detected = True
            if man.detected == True and not(self.attacking):
                if self.right and math.sqrt(pow((man.x - self.x), 2) + pow((man.y - self.y), 2)) <= 10:
                    self.attacking = True

                if self.left and math.sqrt(pow((man.x - self.x), 2) + pow((man.y - self.y), 2)) <= 70:
                    self.attacking = True

                if self.right and math.sqrt(pow((man.x - self.x), 2) + pow((man.y - self.y), 2)) <= 30:
                    self.attacking = True

                if self.y > man.y and not(self.attacking):
                    self.y -= self.vel
                elif self.y < man.y and not(self.attacking):
                    self.y += self.vel

                if self.x > man.x and not(self.attacking): # + self.width:
                    self.x -= self.vel
                    self.left = True
                    self.right = False
                elif self.x < man.x and not(self.attacking): # - self.width/2:
                    self.x += self.vel
                    self.left = False
                    self.right = True
        self.hitboxR = (self.x + 15, self.y, self.width + 5, self.height)
        self.hitboxL = (self.x - 35, self.y, self.width + 15, self.height)

        if self.left:
            self.rect = pygame.Rect(self.x - 35, self.y, self.width, self.height - 10)
        elif self.right:
            self.rect = pygame.Rect(self.x + 15, self.y, self.width, self.height - 10)
        else:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class playerController():
    def __init__(self, player):
        self.player = player

    def movePlayer(self, keys):
        if keys[pygame.K_a] and keys[pygame.K_w] and man.x > 0 and man.y > 0:
            self.player.x -= self.player.vel
            self.player.y -= self.player.vel
            self.player.up = True
            self.player.down = False
            self.player.left = True
            self.player.standing = False
        elif keys[pygame.K_a] and keys[pygame.K_s] and man.x > 0 and man.y < 600 - man.height - 30:
            self.player.x -= self.player.vel
            self.player.y += self.player.vel
            self.player.up = False
            self.player.down = True
            self.player.left = True
            self.player.right = False
            self.player.right = False
            self.player.standing = False
        elif keys[pygame.K_d] and keys[pygame.K_w] and man.x < 800 - man.width and man.y > 0:
            self.player.x += self.player.vel
            self.player.y -= self.player.vel
            self.player.up = True
            self.player.down = False
            self.player.left = False
            self.player.right = True
            self.player.standing = False
        elif keys[pygame.K_d] and keys[pygame.K_s] and man.x < 800 - man.width and man.y < 600 - man.height - 30:
            self.player.x += self.player.vel
            self.player.y += self.player.vel
            self.player.up = False
            self.player.down = True
            self.player.left = False
            self.player.right = True
            self.player.standing = False
        elif keys[pygame.K_a] and man.x > 0:
            self.player.x -= self.player.vel
            self.player.up = False
            self.player.down = False
            self.player.left = True
            self.player.right = False
            self.player.standing = False
        elif keys[pygame.K_d] and man.x < 800 - man.width:
            self.player.x += self.player.vel
            self.player.up = False
            self.player.down = False
            self.player.left = False
            self.player.right = True
            self.player.standing = False
        elif keys[pygame.K_w] and man.y > 0:
            self.player.y -= self.player.vel
            self.player.up = True
            self.player.down = False
            self.player.left = False
            self.player.right = False
            self.player.standing = False
        elif keys[pygame.K_s] and man.y < 600 - man.height - 30:
            self.player.y += self.player.vel
            self.player.up = False
            self.player.down = True
            self.player.left = False
            self.player.right = False
            self.player.standing = False
        else:
            self.player.standing = True

        self.player.hitbox =(man.x + 25, man.y, man.width, man.height)

        def attack(self, attackType):
            #definition here
            return
        def actions(self, actionType):
            #definition here
            return

class gameController():
    def __init__(self, player):
        self.player = player

    def damageTracker(self, window):
        attackers = pygame.sprite.spritecollide(self.player, enemies, False)
        for attacker in attackers:
            if attacker.rect.colliderect(self.player.rect) and not(self.player.damaged) and attacker.Dmg:
                self.player.healthLevel -= 1
                self.player.damaged = True
                attacker.Dmg = False
            else:
                attackers.pop(attackers.index(attacker))
        window.blit(pygame.transform.scale(health[self.player.healthLevel], (135, 150)), (-20,-65))


def loadTileTable(filename, width, height):
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width/width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height/height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table

def redrawGameWindow():
#    window.blit(bg, (0,0))
    window.fill((0,0,0))
#    pygame.draw.rect(window, (255,255,255), (man.x + 25, man.y, man.width, man.height), 1)       #hitbox
#    pygame.draw.rect(window, (255,255,255), (skel.x, skel.y, skel.width, skel.height), 1)   #hitbox
    skel.draw(window)
    skel2.draw(window)
    man.draw(window)
    controlCenter.damageTracker(window)

    pygame.display.update()


skel = skeleton("Skeleton", 700, 100, 64, 64, 1)
skel2 = skeleton("Skeleton", 100, 300, 64, 64, 1)
man = player(200, 410, 32, 80)
control = playerController(man)
controlCenter = gameController(man)
run = True
clock = pygame.time.Clock()
while run:
    clock.tick(50)                                  #framerate

    keys = pygame.key.get_pressed()                 #keylistener

    control.movePlayer(keys)

    skel.move()
    skel2.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #quit

    redrawGameWindow()

pygame.quit()
