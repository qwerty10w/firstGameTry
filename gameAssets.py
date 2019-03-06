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
        self.Pwr = 1
        self.left = False
        self.right = False
        self.up = False
        self.down = True
        self.walkCount = 0
        self.attackCount = 0
        self.standing = True
        self.attacking = False
        self.healthLevel = 5
        self.detected = False
        self.damaged  = False
        self.hitbox = (self.x + 25, self.y, self.width, self.height)
        self.rect = pygame.Rect(self.x + 25, self.y, self.width, self.height)
        self.attackRect = pygame.Rect(self.x, self.y - 12, 80, 32)
    def draw(self, window):
        if self.walkCount + 1 > 30:
            self.walkCount = 0
        if self.attackCount + 1 > 30:
            self.attackCount = 0
            self.attacking = False
        if self.attacking:
            if self.right:
                window.blit(attackRight[self.attackCount//10], (self.x + 18,self.y))
                self.attackCount +=2
                if self.attackCount//10 == 1:
                    pygame.draw.rect(window, (255,255,255), self.attackRect, 1)
            elif self.left:
                window.blit(attackLeft[self.attackCount//10], (self.x - 18,self.y))
                self.attackCount +=2
                if self.attackCount//10 == 1:
                    pygame.draw.rect(window, (255,255,255), self.attackRect, 1)
            elif self.up:
                window.blit(attackUp[self.attackCount//10], (self.x, self.y))
                self.attackCount +=2
                if self.attackCount//10 == 1:
                    pygame.draw.rect(window, (255,255,255), self.attackRect, 1)
            elif self.down:
                window.blit(attackDown[self.attackCount//10], (self.x, self.y))
                self.attackCount +=2
                if self.attackCount//10 == 1:
                    pygame.draw.rect(window, (255,255,255), self.attackRect, 1)
        elif not(self.standing) and not(self.attacking):
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
            if not(self.attacking):
                if self.left:
                    window.blit(walkLeft[0], (self.x, self.y))
                if self.right:
                    window.blit(walkRight[0], (self.x, self.y))
                if self.down:
                    window.blit(idle[self.walkCount//6], (self.x,self.y))
                    self.walkCount +=1
                if self.up:
                    window.blit(pygame.image.load("Assets/Player/knight iso char_idle up_0.png"), (self.x, self.y))

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
        self.hitCount = 0
        self.standing = True
        self.attacking = False
        self.Dmg = False
        self.damaged = False
        self.Pwr = 1
        self.healthLevel = 5

    def printType(self):
        print(self.type)

class skeleton(enemy):
    def __init__(self, type, x, y, width, height, vel):
        super().__init__(type, x, y, width, height, vel)
        self.attackRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.healthLevel = 2
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
            if self.hitCount + 1 > 24:
                self.hitCount = 0
                self.damaged = False
                self.attacking = False
                self.standing = True
                # self.left = False
                # self.right = False

            if self.damaged:
                self.attacking = False
                self.attackCount = 0
                self.Dmg = False
                if self.right:
                    window.blit(pygame.transform.scale2x(skelHit[self.hitCount//3]), (self.x - 12, self.y + 3))
                    self.hitCount += 1
                elif self.left:
                    window.blit(pygame.transform.flip(pygame.transform.scale2x(skelHit[self.hitCount//3]), True, False), (self.x - 3, self.y + 3))
                    self.hitCount += 1

            if self.attacking:
                if self.right:
                    window.blit(pygame.transform.scale2x(skelAttack[self.attackCount//3]), (self.x, self.y - 9))
                    self.attackCount += 1
                    self.Dmg = False
                    if self.attackCount >= 24 and self.attackCount <= 33:
                        pygame.draw.rect(window, (255,255,255), self.attackRect, 1) #hitbox
                        self.Dmg = True

                elif self.left:
                    window.blit(pygame.transform.scale2x(pygame.transform.flip(skelAttack[self.attackCount//3], True, False)), (self.x - 40, self.y - 9))
                    self.attackCount += 1
                    self.Dmg = False
                    if self.attackCount >= 24 and self.attackCount <= 33:
                        pygame.draw.rect(window, (255,255,255), self.attackRect, 1) #hitbox
                        self.Dmg = True

            if not(self.standing) and not(self.attacking) and not(self.damaged):
                if self.left:
                    window.blit(pygame.transform.scale2x(pygame.transform.flip(skelWalkRight[self.walkCount//3], True, False)), (self.x,self.y))
                    self.walkCount += 1
                if self.right:
                    window.blit(pygame.transform.scale2x(skelWalkRight[self.walkCount//3]), (self.x,self.y))
                    self.walkCount += 1
            elif self.standing:
                if self.right:
                    window.blit(pygame.transform.scale2x(skelIdle[self.walkCount//4]), (self.x,self.y))
                    self.walkCount += 1
                elif self.left:
                    window.blit(pygame.transform.flip(pygame.transform.scale2x(skelIdle[self.walkCount//4]), True, False), (self.x,self.y))
                    self.walkCount += 1
    def move(self):
        if self.standing:
            if self.x > man.x:
                self.left = True
                self.right = False
            else:
                self.left = False
                self.right = True
        if (math.sqrt(pow((man.x - self.x), 2) + pow((man.y - self.y), 2)) <= 425):
            self.standing = False
            man.detected = True
            if man.detected == True and not(self.attacking) and not(self.damaged):
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

        if self.left:
            self.attackRect = pygame.Rect(self.x - 35, self.y, self.width, self.height)
        elif self.right:
            self.attackRect = pygame.Rect(self.x + 35, self.y, self.width, self.height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class playerController():
    def __init__(self, player):
        self.player = player

    def movePlayer(self, keys):
        if keys[pygame.K_j]:
            self.player.attacking = True
        elif not(self.player.attacking):
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

        self.player.rect = pygame.Rect(self.player.x + 25, self.player.y, self.player.width, self.player.height)
        if self.player.right:
            self.player.attackRect = pygame.Rect(self.player.x + self.player.width + 7, self.player.y + (self.player.height/2), 60, 32)
        elif self.player.left:
            self.player.attackRect = pygame.Rect(self.player.x - self.player.width + 7, self.player.y + (self.player.height/2), 60, 32)
        elif self.player.up:
            self.player.attackRect = pygame.Rect(self.player.x, self.player.y - 3, 80, 32)
        elif self.player.down:
            self.player.attackRect = pygame.Rect(self.player.x, self.player.y + 40, 80, 32)

        def actions(self, actionType):
            #definition here
            return

class gameController():
    def __init__(self, player):
        self.player = player

    def damageTracker(self, window):
        for attacker in enemies:
            if attacker.attackRect.colliderect(self.player.rect) and not(self.player.damaged) and attacker.Dmg:
                self.player.healthLevel -= attacker.Pwr
                self.player.damaged = True
                attacker.Dmg = False
                print("player hit")
            if self.player.attackRect.colliderect(attacker.rect) and not(attacker.damaged) and self.player.attacking:
                if not(attacker.damaged):
                    attacker.healthLevel -= self.player.Pwr
                    attacker.damaged = True
                    attacker.attacking = False
                    print("hit")
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
    pygame.draw.rect(window, (255,255,255), man.rect, 1)       #hitbox
    pygame.draw.rect(window, (255,255,255), skel.rect, 1)   #hitbox
    skel.draw(window)
    skel2.draw(window)
    man.draw(window)
    controlCenter.damageTracker(window)

    pygame.display.update()


skel = skeleton("Skeleton", 700, 100, 50, 64, 1)
skel2 = skeleton("Skeleton", 100, 300, 50, 64, 0)
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
