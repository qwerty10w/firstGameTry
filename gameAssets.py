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
        self.vel = 1.25
        self.left = False
        self.right = False
        self.up = False
        self.down = True
        self.walkCount = 0
        self.standing = True
        self.attacking = False
        self.healthLevel = 5
        self.detected = False

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
        self.healthLevel = 5

class enemyController():
    def __init__(self, enemy):
        self.enemy = enemy

    def draw(self, window):
        if self.enemy.type == "Skeleton":
            if self.enemy.walkCount + 1 > 36:
                self.enemy.walkCount = 0
            if self.enemy.attackCount + 1 > 54:
                self.enemy.attackCount = 0
                self.enemy.attacking = False
                self.enemy.left = False
                self.enemy.right = False
                #self.enemy.standing = True

            if self.enemy.attacking and self.enemy.right:
                window.blit(pygame.transform.scale2x(skelAttack[self.enemy.attackCount//3]), (self.enemy.x, self.enemy.y - 9))
                self.enemy.attackCount += 1
                if self.enemy.attackCount >= 24 and self.enemy.attackCount <= 33:
                    pygame.draw.rect(window, (255,255,255), (self.enemy.x + 20, self.enemy.y, 64, 64), 1)

            elif self.enemy.attacking and self.enemy.left:
                window.blit(pygame.transform.scale2x(pygame.transform.flip(skelAttack[self.enemy.attackCount//3], True, False)), (self.enemy.x - 40, self.enemy.y - 9))
                self.enemy.attackCount += 1
                if self.enemy.attackCount >= 24 and self.enemy.attackCount <= 33:
                    pygame.draw.rect(window, (255,255,255), (self.enemy.x - 35, self.enemy.y, 64, 64), 1)

            if not(self.enemy.standing) and not(self.enemy.attacking):
                if self.enemy.left:
                    window.blit(pygame.transform.scale2x(pygame.transform.flip(skelWalkRight[self.enemy.walkCount//3], True, False)), (self.enemy.x,self.enemy.y))
                    self.enemy.walkCount += 1
                if self.enemy.right:
                    window.blit(pygame.transform.scale2x(skelWalkRight[self.enemy.walkCount//3]), (self.enemy.x,self.enemy.y))
                    self.enemy.walkCount += 1
            elif self.enemy.standing:
                window.blit(pygame.transform.scale2x(skelIdle[self.enemy.walkCount//4]), (self.enemy.x,self.enemy.y))
                self.enemy.walkCount += 1

    def moveEnemy(self):
        if self.enemy.type == "Skeleton":
            if (math.sqrt(pow((man.x - self.enemy.x), 2) + pow((man.y - self.enemy.y), 2)) <= 425):
                self.enemy.standing = False
                man.detected = True
                if man.detected == True and not(self.enemy.attacking):
                    if self.enemy.right and math.sqrt(pow((man.x - self.enemy.x), 2) + pow((man.y - self.enemy.y), 2)) <= 10:
                        self.enemy.attacking = True

                    if self.enemy.left and math.sqrt(pow((man.x - self.enemy.x), 2) + pow((man.y - self.enemy.y), 2)) <= 70:
                        self.enemy.attacking = True

                    if self.enemy.right and math.sqrt(pow((man.x - self.enemy.x), 2) + pow((man.y - self.enemy.y), 2)) <= 30:
                        self.enemy.attacking = True

                    if self.enemy.y > man.y and not(self.enemy.attacking):
                        self.enemy.y -= self.enemy.vel
                    elif self.enemy.y < man.y and not(self.enemy.attacking):
                        self.enemy.y += self.enemy.vel

                    if self.enemy.x > man.x and not(self.enemy.attacking): # + self.enemy.width:
                        self.enemy.x -= self.enemy.vel
                        self.enemy.left = True
                        self.enemy.right = False
                    elif self.enemy.x < man.x and not(self.enemy.attacking): # - self.enemy.width/2:
                        self.enemy.x += self.enemy.vel
                        self.enemy.left = False
                        self.enemy.right = True

class Controller():
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

    def damageTracker(self, window):
        window.blit(pygame.transform.scale(health[self.player.healthLevel], (135, 150)), (-20,-65))

def redrawGameWindow():
#    window.blit(bg, (0,0))
    window.fill((0,0,0))
    pygame.draw.rect(window, (255,255,255), (man.x + 25, man.y, man.width, man.height), 1)       #hitbox
    #pygame.draw.rect(window, (255,255,255), (skel.x, skel.y, skel.width, skel.height), 1)   #hitbox
    enemyController.draw(window)
    man.draw(window)
    control.damageTracker(window)

    pygame.display.update()


skel = enemy("Skeleton", 700, 100, 64, 64, 1)
man = player(200, 410, 32, 80)
control = Controller(man)
enemyController = enemyController(skel)
run = True
clock = pygame.time.Clock()
while run:
    clock.tick(50)                                  #framerate

    keys = pygame.key.get_pressed()                 #keylistener

    control.movePlayer(keys)
#    control.damageTracker()

    enemyController.moveEnemy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #quit

    redrawGameWindow()

pygame.quit()
