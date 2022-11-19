import pygame, sys, math
import pygame as pygame
from pygame.locals import *
from settings import *
from level import Level
from gamedata import level_0
import random

from Classes.RainDrop import RainDrop

#Score
def display_score():

    current_time = int(pygame.time.get_ticks() /1000) -start_time
    score_surf = test_font.render(f'Score: {current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in  obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]


#Common
pygame.init()
pygame.display.set_caption('Runner')  #title of the game*
game_active = False
start_time = 0
score = 0


#Screen
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_0, screen)

#Background
sky_surface = pygame.image.load('graphics/background/Sky.png').convert()
ground_surface = pygame.image.load('graphics/background/ground.png').convert()

#Score
test_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
#score_surf = test_font.render('My game', False, ( 64 , 64, 64))
#score_rect = score_surf.get_rect(center = (400, 50))

#Player

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0


#Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner', False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run', False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400, 320))


snail_x_pos = 600

#Obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surf =pygame.image.load('graphics/fly/Fly1.png').convert_alpha()

obstacle_rect_list  = []

#Rain
image2 = pygame.image.load("graphics/rain/raindrop.png")
raindrop_group = pygame.sprite.Group()

for raindrop in range(20):

    new_raindrop = RainDrop("graphics/rain/raindrop.png",random.randrange(0,screen_width),random.randrange(0,screen_height))
    raindrop_group.add(new_raindrop)

#Timer
obstacle_timer = pygame.USEREVENT + 1 #reserved events no conflicts + 1
pygame.time.set_timer(obstacle_timer, 1400)



while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            #jumping
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = - 20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = - 20

        else:  #when we restart the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() /1000) -start_time
        if event.type  == obstacle_timer and game_active:
            if random.randrange(0,2):
                 obstacle_rect_list.append(snail_surface.get_rect(bottomright = (random.randrange(900,1100) ,300)))
            else:
                 obstacle_rect_list.append(fly_surf.get_rect(bottomright=(random.randrange(900, 1100), 210)))
    if game_active:
        screen.blit(ground_surface, (0, 300))
        screen.blit(sky_surface, (0, 0))
        display_score()

        score = display_score()
        #Player
        player_gravity += 1

        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        raindrop_group.draw(screen)

        keys = pygame.key.get_pressed()

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity =0

        screen.blit(game_name, game_name_rect)
        score_message = test_font.render(f'Your score: {score}', False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)


    pygame.display.update()
    clock.tick(60)  #runs 60 times per second , so itsnot fast or slow