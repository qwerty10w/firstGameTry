import pygame
import pytmx
pygame.font.init()

#Map Assets
#gameMap = pytmx.load_pygame("Assets/DungeonAssets/character and tileset/Map.tmx")

#Skeleton Assets
skelWalkRight = [pygame.image.load("Assets/Skeletons/Walking_0.gif"), pygame.image.load("Assets/Skeletons/Walking_1.gif"), pygame.image.load("Assets/Skeletons/Walking_2.gif"), pygame.image.load("Assets/Skeletons/Walking_3.gif"), pygame.image.load("Assets/Skeletons/Walking_4.gif"), pygame.image.load("Assets/Skeletons/Walking_5.gif"), pygame.image.load("Assets/Skeletons/Walking_6.gif"), pygame.image.load("Assets/Skeletons/Walking_7.gif"), pygame.image.load("Assets/Skeletons/Walking_8.gif"), pygame.image.load("Assets/Skeletons/Walking_9.gif"), pygame.image.load("Assets/Skeletons/Walking_10.gif"), pygame.image.load("Assets/Skeletons/Walking_11.gif"), pygame.image.load("Assets/Skeletons/Walking_12.gif") ]
skelIdle = [pygame.image.load("Assets/Skeletons/Idle_0.gif"), pygame.image.load("Assets/Skeletons/Idle_1.gif"), pygame.image.load("Assets/Skeletons/Idle_2.gif"), pygame.image.load("Assets/Skeletons/Idle_3.gif"), pygame.image.load("Assets/Skeletons/Idle_4.gif"), pygame.image.load("Assets/Skeletons/Idle_5.gif"), pygame.image.load("Assets/Skeletons/Idle_6.gif"), pygame.image.load("Assets/Skeletons/Idle_7.gif"), pygame.image.load("Assets/Skeletons/Idle_8.gif"), pygame.image.load("Assets/Skeletons/Idle_9.gif"), pygame.image.load("Assets/Skeletons/Idle_10.gif")]
skelAttack = [pygame.image.load("Assets/Skeletons/Attack_0.gif"), pygame.image.load("Assets/Skeletons/Attack_1.gif"), pygame.image.load("Assets/Skeletons/Attack_2.gif"), pygame.image.load("Assets/Skeletons/Attack_3.gif"), pygame.image.load("Assets/Skeletons/Attack_4.gif"), pygame.image.load("Assets/Skeletons/Attack_5.gif"), pygame.image.load("Assets/Skeletons/Attack_6.gif"), pygame.image.load("Assets/Skeletons/Attack_7.gif"), pygame.image.load("Assets/Skeletons/Attack_8.gif"), pygame.image.load("Assets/Skeletons/Attack_9.gif"), pygame.image.load("Assets/Skeletons/Attack_10.gif"), pygame.image.load("Assets/Skeletons/Attack_11.gif"), pygame.image.load("Assets/Skeletons/Attack_12.gif"), pygame.image.load("Assets/Skeletons/Attack_13.gif"), pygame.image.load("Assets/Skeletons/Attack_14.gif"), pygame.image.load("Assets/Skeletons/Attack_15.gif"), pygame.image.load("Assets/Skeletons/Attack_16.gif"), pygame.image.load("Assets/Skeletons/Attack_17.gif")]
skelHit = [pygame.image.load("Assets/Skeletons/Hit_0.gif"), pygame.image.load("Assets/Skeletons/Hit_1.gif"), pygame.image.load("Assets/Skeletons/Hit_2.gif"), pygame.image.load("Assets/Skeletons/Hit_3.gif"), pygame.image.load("Assets/Skeletons/Hit_4.gif"), pygame.image.load("Assets/Skeletons/Hit_5.gif"), pygame.image.load("Assets/Skeletons/Hit_6.gif"), pygame.image.load("Assets/Skeletons/Hit_7.gif")]
skelDeath = [pygame.image.load("Assets/Skeletons/Death_0.gif"), pygame.image.load("Assets/Skeletons/Death_1.gif"), pygame.image.load("Assets/Skeletons/Death_2.gif"), pygame.image.load("Assets/Skeletons/Death_3.gif"), pygame.image.load("Assets/Skeletons/Death_4.gif"), pygame.image.load("Assets/Skeletons/Death_5.gif"), pygame.image.load("Assets/Skeletons/Death_6.gif"), pygame.image.load("Assets/Skeletons/Death_7.gif"), pygame.image.load("Assets/Skeletons/Death_8.gif"), pygame.image.load("Assets/Skeletons/Death_9.gif"), pygame.image.load("Assets/Skeletons/Death_10.gif"), pygame.image.load("Assets/Skeletons/Death_11.gif"), pygame.image.load("Assets/Skeletons/Death_12.gif"), pygame.image.load("Assets/Skeletons/Death_13.gif"), pygame.image.load("Assets/Skeletons/Death_14.gif") ]


#Player Assets
walkRight =[pygame.image.load("Assets/Player/knight iso char_run right_0.png"), pygame.image.load("Assets/Player/knight iso char_run right_1.png"), pygame.image.load("Assets/Player/knight iso char_run right_2.png"), pygame.image.load("Assets/Player/knight iso char_run right_3.png"), pygame.image.load("Assets/Player/knight iso char_run right_4.png"), pygame.image.load("Assets/Player/knight iso char_run right_5.png")]
walkLeft = [pygame.image.load("Assets/Player/knight iso char_run left_0.png"), pygame.image.load("Assets/Player/knight iso char_run left_1.png"), pygame.image.load("Assets/Player/knight iso char_run left_2.png"), pygame.image.load("Assets/Player/knight iso char_run left_3.png"), pygame.image.load("Assets/Player/knight iso char_run left_4.png"), pygame.image.load("Assets/Player/knight iso char_run left_5.png")]
walkUp = [pygame.image.load("Assets/Player/knight iso char_run up_0.png"), pygame.image.load("Assets/Player/knight iso char_run up_1.png"), pygame.image.load("Assets/Player/knight iso char_run up_2.png"), pygame.image.load("Assets/Player/knight iso char_run up_3.png"), pygame.image.load("Assets/Player/knight iso char_run up_4.png"), pygame.image.load("Assets/Player/knight iso char_run up_4.png")]
walkDown = [pygame.image.load("Assets/Player/knight iso char_run down_0.png"), pygame.image.load("Assets/Player/knight iso char_run down_1.png"), pygame.image.load("Assets/Player/knight iso char_run down_2.png"), pygame.image.load("Assets/Player/knight iso char_run down_3.png"), pygame.image.load("Assets/Player/knight iso char_run down_4.png"), pygame.image.load("Assets/Player/knight iso char_run down_4.png")]
attackLeft = [pygame.image.load("Assets/Player/knight iso char_slice right_0.png"), pygame.image.load("Assets/Player/knight iso char_slice right_1.png"), pygame.image.load("Assets/Player/knight iso char_slice right_2.png")]
attackRight = [pygame.image.load("Assets/Player/knight iso char_slice left_0.png"), pygame.image.load("Assets/Player/knight iso char_slice left_1.png"), pygame.image.load("Assets/Player/knight iso char_slice left_2.png")]
attackUp = [pygame.image.load("Assets/Player/knight iso char_slice up_0.png"), pygame.image.load("Assets/Player/knight iso char_slice up_1.png"), pygame.image.load("Assets/Player/knight iso char_slice up_2.png")]
attackDown = [pygame.image.load("Assets/Player/knight iso char_slice down_0.png"), pygame.image.load("Assets/Player/knight iso char_slice down_1.png"), pygame.image.load("Assets/Player/knight iso char_slice down_2.png")]
idle = [pygame.image.load("Assets/Player/knight iso char_idle_0.png"), pygame.image.load("Assets/Player/knight iso char_idle_1.png"), pygame.image.load("Assets/Player/knight iso char_idle_2.png"), pygame.image.load("Assets/Player/knight iso char_idle_3.png"), pygame.image.load("Assets/Player/knight iso char_idle_3.png"), pygame.image.load("Assets/Player/knight iso char_idle_3.png")]
health = [pygame.image.load("Assets/Dungeon/HP_Value_0.png"), pygame.image.load("Assets/Dungeon/HP_Value_1.png"), pygame.image.load("Assets/Dungeon/HP_Value_2.png"), pygame.image.load("Assets/Dungeon/HP_Value_3.png"), pygame.image.load("Assets/Dungeon/HP_Value_4.png"), pygame.image.load("Assets/Dungeon/HP_Value_5.png")]

#Menu Assets
menuWindow = pygame.image.load("Assets/Menu Window.png")
font = pygame.font.Font('Assets/pixelFont.ttf', 48)
