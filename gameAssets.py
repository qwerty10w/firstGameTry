import pygame
pygame.init()
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("First Game")

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
        self.isJump = False
        self.left = False
        self.right = False
        self.up = False
        self.down = True
        self.walkCount = 0
        self.standing = True
        self.healthLevel = 5

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
#            self.player.down = False
#            self.player.up = False
#            self.player.left = False
#            self.player.right = False
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
    control.damageTracker(window)
    pygame.display.update()


man = player(200, 410, 64,64)
control = Controller(man)
run = True
clock = pygame.time.Clock()
while run:
    clock.tick(50)                                  #framerate

    keys = pygame.key.get_pressed()                 #keylistener

    control.movePlayer(keys)
#    control.damageTracker()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #quit

    redrawGameWindow()

pygame.quit()
