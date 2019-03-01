import math
import pygame
pygame.init()
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("First Game")

#Skeleton Assets
skelWalkRight = [pygame.image.load("Assets/Skeletons/Walking_0.gif"), pygame.image.load("Assets/Skeletons/Walking_1.gif"), pygame.image.load("Assets/Skeletons/Walking_2.gif"), pygame.image.load("Assets/Skeletons/Walking_3.gif"), pygame.image.load("Assets/Skeletons/Walking_4.gif"), pygame.image.load("Assets/Skeletons/Walking_5.gif"), pygame.image.load("Assets/Skeletons/Walking_6.gif"), pygame.image.load("Assets/Skeletons/Walking_7.gif"), pygame.image.load("Assets/Skeletons/Walking_8.gif"), pygame.image.load("Assets/Skeletons/Walking_9.gif"), pygame.image.load("Assets/Skeletons/Walking_10.gif"), pygame.image.load("Assets/Skeletons/Walking_11.gif"), pygame.image.load("Assets/Skeletons/Walking_12.gif") ]
skelIdle = pygame.image.load("Assets/Skeletons/Skeleton Idle.gif")
skelAttack = [pygame.image.load("Assets/Skeletons/Attack_0.gif"), pygame.image.load("Assets/Skeletons/Attack_1.gif"), pygame.image.load("Assets/Skeletons/Attack_2.gif"), pygame.image.load("Assets/Skeletons/Attack_3.gif"), pygame.image.load("Assets/Skeletons/Attack_4.gif"), pygame.image.load("Assets/Skeletons/Attack_5.gif"), pygame.image.load("Assets/Skeletons/Attack_6.gif"), pygame.image.load("Assets/Skeletons/Attack_7.gif"), pygame.image.load("Assets/Skeletons/Attack_8.gif"), pygame.image.load("Assets/Skeletons/Attack_9.gif"), pygame.image.load("Assets/Skeletons/Attack_10.gif"), pygame.image.load("Assets/Skeletons/Attack_11.gif"), pygame.image.load("Assets/Skeletons/Attack_12.gif"), pygame.image.load("Assets/Skeletons/Attack_13.gif"), pygame.image.load("Assets/Skeletons/Attack_14.gif"), pygame.image.load("Assets/Skeletons/Attack_15.gif"), pygame.image.load("Assets/Skeletons/Attack_16.gif"), pygame.image.load("Assets/Skeletons/Attack_17.gif")]

#Player Assets
walkRight =[pygame.image.load("Assets/Player/knight iso char_run right_0.png"), pygame.image.load("Assets/Player/knight iso char_run right_1.png"), pygame.image.load("Assets/Player/knight iso char_run right_2.png"), pygame.image.load("Assets/Player/knight iso char_run right_3.png"), pygame.image.load("Assets/Player/knight iso char_run right_4.png"), pygame.image.load("Assets/Player/knight iso char_run right_5.png")]
walkLeft = [pygame.image.load("Assets/Player/knight iso char_run left_0.png"), pygame.image.load("Assets/Player/knight iso char_run left_1.png"), pygame.image.load("Assets/Player/knight iso char_run left_2.png"), pygame.image.load("Assets/Player/knight iso char_run left_3.png"), pygame.image.load("Assets/Player/knight iso char_run left_4.png"), pygame.image.load("Assets/Player/knight iso char_run left_5.png")]
walkUp = [pygame.image.load("Assets/Player/knight iso char_run up_0.png"), pygame.image.load("Assets/Player/knight iso char_run up_1.png"), pygame.image.load("Assets/Player/knight iso char_run up_2.png"), pygame.image.load("Assets/Player/knight iso char_run up_3.png"), pygame.image.load("Assets/Player/knight iso char_run up_4.png"), pygame.image.load("Assets/Player/knight iso char_run up_4.png")]
walkDown = [pygame.image.load("Assets/Player/knight iso char_run down_0.png"), pygame.image.load("Assets/Player/knight iso char_run down_1.png"), pygame.image.load("Assets/Player/knight iso char_run down_2.png"), pygame.image.load("Assets/Player/knight iso char_run down_3.png"), pygame.image.load("Assets/Player/knight iso char_run down_4.png"), pygame.image.load("Assets/Player/knight iso char_run down_4.png")]
idle = [pygame.image.load("Assets/Player/knight iso char_idle_0.png"), pygame.image.load("Assets/Player/knight iso char_idle_1.png"), pygame.image.load("Assets/Player/knight iso char_idle_2.png"), pygame.image.load("Assets/Player/knight iso char_idle_3.png"), pygame.image.load("Assets/Player/knight iso char_idle_3.png"), pygame.image.load("Assets/Player/knight iso char_idle_3.png")]

health = [pygame.image.load("Assets/Dungeon/HP_Value_0.png"), pygame.image.load("Assets/Dungeon/HP_Value_1.png"), pygame.image.load("Assets/Dungeon/HP_Value_2.png"), pygame.image.load("Assets/Dungeon/HP_Value_3.png"), pygame.image.load("Assets/Dungeon/HP_Value_4.png"), pygame.image.load("Assets/Dungeon/HP_Value_5.png")]

class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
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

            if self.enemy.attacking and self.enemy.right:
                window.blit(pygame.transform.scale(skelAttack[self.enemy.walkCount//3], (50,64)), (self.enemy.x,self.enemy.y))
                self.enemy.walkCount += 1
            elif self.enemy.attacking and self.enemy.left:
                window.blit(pygame.transform.flip(pygame.transform.scale(skelAttack[self.enemy.walkCount//3], (50,64)), True, False), (self.enemy.x,self.enemy.y))
                self.enemy.walkCount += 1

            if not(self.enemy.standing) and not(self.enemy.attacking):
                if self.enemy.left:
                    window.blit(pygame.transform.scale(pygame.transform.flip(skelWalkRight[self.enemy.walkCount//3], True, False), (50,64)), (self.enemy.x,self.enemy.y))
                    self.enemy.walkCount += 1
                if self.enemy.right:
                    window.blit(pygame.transform.scale(skelWalkRight[self.enemy.walkCount//3], (50,64)), (self.enemy.x,self.enemy.y))
                    self.enemy.walkCount += 1
            elif self.enemy.standing:
                window.blit(pygame.transform.scale(skelIdle, (50,64)), (self.enemy.x,self.enemy.y))


    def moveEnemy(self):
        if self.enemy.type == "Skeleton":
            if (math.sqrt(pow((man.x - self.enemy.x), 2) + pow((man.y - self.enemy.y), 2)) <= 425):
                self.enemy.standing = False
                man.detected = True
                if man.detected == True and not(self.enemy.attacking):

                    if self.enemy.right:
                        if(math.sqrt(pow((man.x - self.enemy.x), 2) + pow((man.y - self.enemy.y), 2)) <= 70):
                            self.enemy.attacking = True

                    if(math.sqrt(pow((man.x - self.enemy.x), 2) + pow((man.y - self.enemy.y), 2)) <= 70):
                        self.enemy.attacking = True

                    if self.enemy.y > man.y and not(self.enemy.standing):
                        self.enemy.y -= self.enemy.vel
                    elif self.enemy.y < man.y and not(self.enemy.standing):
                        self.enemy.y += self.enemy.vel

                    if self.enemy.x > man.x and not(self.enemy.standing): # + self.enemy.width:
                        self.enemy.x -= self.enemy.vel
                        self.enemy.left = True
                        self.enemy.right = False
                    elif self.enemy.x < man.x and not(self.enemy.standing): # - self.enemy.width/2:
                        self.enemy.x += self.enemy.vel
                        self.enemy.left = False
                        self.enemy.right = True

#                if self.enemy.x == man.x and self.enemy.y == man.y:
#                    self.enemy.standing = True
            else:
                self.enemy.standing = True

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
    man.draw(window)
    pygame.draw.rect(window, (255,255,255), (man.x, man.y, man.width, man.height), 1)       #hitbox
    pygame.draw.rect(window, (255,255,255), (skel.x, skel.y, skel.width, skel.height), 1)   #hitbox
    enemyController.draw(window)
    control.damageTracker(window)

    pygame.display.update()


man = player(200, 410, 64,64)
skel = enemy("Skeleton", 700, 100, 64, 64, 1)
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
