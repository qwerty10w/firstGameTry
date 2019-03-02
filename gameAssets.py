import math
import pygame
from resources import *
pygame.init()
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("First Game")

class player():
    def __init__(self, x, y, width, height):
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

class enemy():
    def __init__(self, type, x, y, width, height, vel):
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
                #self.standing = True

            if self.attacking and self.right:
                window.blit(pygame.transform.scale2x(skelAttack[self.attackCount//3]), (self.x, self.y - 9))
                self.attackCount += 1
                if self.attackCount >= 24 and self.attackCount <= 33:
                    #pygame.draw.rect(window, (255,255,255), (self.x + 20, self.y, 64, 64), 1) #hitbox
                    self.Dmg = True


            elif self.attacking and self.left:
                window.blit(pygame.transform.scale2x(pygame.transform.flip(skelAttack[self.attackCount//3], True, False)), (self.x - 40, self.y - 9))
                self.attackCount += 1
                if self.attackCount >= 24 and self.attackCount <= 33:
                    #pygame.draw.rect(window, (255,255,255), (self.x - 35, self.y, 64, 64), 1) #hitbox
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

class playerController():
    def __init__(self, player):
        self.player = player

    def movePlayer(self, keys):
        if keys[pygame.K_LEFT] and keys[pygame.K_UP] and man.x > 0 and man.y > 0:
            self.player.x -= self.player.vel
            self.player.y -= self.player.vel
            self.player.up = True
            self.player.down = False
            self.player.left = True
            self.player.standing = False
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN] and man.x > 0 and man.y < 600 - man.height - 30:
            self.player.x -= self.player.vel
            self.player.y += self.player.vel
            self.player.up = False
            self.player.down = True
            self.player.left = True
            self.player.right = False
            self.player.right = False
            self.player.standing = False
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP] and man.x < 800 - man.width and man.y > 0:
            self.player.x += self.player.vel
            self.player.y -= self.player.vel
            self.player.up = True
            self.player.down = False
            self.player.left = False
            self.player.right = True
            self.player.standing = False
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] and man.x < 800 - man.width and man.y < 600 - man.height - 30:
            self.player.x += self.player.vel
            self.player.y += self.player.vel
            self.player.up = False
            self.player.down = True
            self.player.left = False
            self.player.right = True
            self.player.standing = False
        elif keys[pygame.K_LEFT] and man.x > 0:
            self.player.x -= self.player.vel
            self.player.up = False
            self.player.down = False
            self.player.left = True
            self.player.right = False
            self.player.standing = False
        elif keys[pygame.K_RIGHT] and man.x < 800 - man.width:
            self.player.x += self.player.vel
            self.player.up = False
            self.player.down = False
            self.player.left = False
            self.player.right = True
            self.player.standing = False
        elif keys[pygame.K_UP] and man.y > 0:
            self.player.y -= self.player.vel
            self.player.up = True
            self.player.down = False
            self.player.left = False
            self.player.right = False
            self.player.standing = False
        elif keys[pygame.K_DOWN] and man.y < 600 - man.height - 30:
            self.player.y += self.player.vel
            self.player.up = False
            self.player.down = True
            self.player.left = False
            self.player.right = False
            self.player.standing = False
        else:
            self.player.standing = True

        def attack(self, attackType):
            #definition here
            return
        def actions(self, actionType):
            #definition here
            return

class gameController():
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def damageTracker(self, window):
        if self.player.x + self.player.width + 25 >= self.enemy.x - 35 and self.player.x + self.player.width + 25 <= self.enemy.x + 20 + self.enemy.width and ((self.player.y >= self.enemy.y and self.player.y <= self.enemy.y + self.enemy.height) or (self.player.y + self.player.height/2 >= self.enemy.y and self.player.y + self.player.height/2 <= self.enemy.y + self.enemy.height) or (self.player.y + self.player.height >= self.enemy.y and self.player.y + self.player.height <= self.enemy.y + self.enemy.height)) and self.enemy.Dmg and not(self.player.damaged):
            self.player.healthLevel -= 1
            self.player.damaged = True
        elif self.player.x + 25 >= self.enemy.x - 35 and self.player.x + 25 <= self.enemy.x + 20 + self.enemy.width and ((self.player.y >= self.enemy.y and self.player.y <= self.enemy.y + self.enemy.height) or (self.player.y + self.player.height/2 >= self.enemy.y and self.player.y + self.player.height/2 <= self.enemy.y + self.enemy.height) or (self.player.y + self.player.height >= self.enemy.y and self.player.y + self.player.height <= self.enemy.y + self.enemy.height)) and self.enemy.Dmg and not(self.player.damaged):
            self.player.healthLevel -= 1
            self.player.damaged = True
        window.blit(pygame.transform.scale(health[self.player.healthLevel], (135, 150)), (-20,-65))
        self.enemy.Dmg = False

def redrawGameWindow():
#    window.blit(bg, (0,0))
    window.fill((0,0,0))
    #pygame.draw.rect(window, (255,255,255), (man.x + 25, man.y, man.width, man.height), 1)       #hitbox
    #pygame.draw.rect(window, (255,255,255), (skel.x, skel.y, skel.width, skel.height), 1)   #hitbox
    skel.draw(window)
    man.draw(window)
    controlCenter.damageTracker(window)

    pygame.display.update()


skel = skeleton("Skeleton", 700, 100, 64, 64, 1)
man = player(200, 410, 32, 80)
control = playerController(man)
controlCenter = gameController(man, skel)
run = True
clock = pygame.time.Clock()
while run:
    clock.tick(50)                                  #framerate

    keys = pygame.key.get_pressed()                 #keylistener

    control.movePlayer(keys)

    skel.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #quit

    redrawGameWindow()

pygame.quit()
