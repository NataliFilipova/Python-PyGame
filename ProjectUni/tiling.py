import pygame, sys
from settings import *
from level import Level
from gamedata import level_0

def display_score():

    current_time = int(pygame.time.get_ticks() /1000) -start_time
    score_surf = test_font.render(f'Score: {current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time


pygame.init()
pygame.display.set_caption('Runner')  #title of the game*
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_0,screen)
game_active = False
start_time = 0
score = 0

test_font = pygame.font.Font('Font/Pixeltype.ttf', 70)
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0,2)
player_stand_rect = player_stand.get_rect(center = (600,400))

game_name = test_font.render('Pixel Runner', False,(111,196,169))
game_name_rect = game_name.get_rect(center = (600,200))

game_message = test_font.render('Press space to run', False,(111,196,169))
game_message_rect = game_message.get_rect(center = (600, 250))

obstacle_timer = pygame.USEREVENT + 1 #reserved events no conflicts + 1
pygame.time.set_timer(obstacle_timer, 1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000) - start_time
    if game_active:
     screen.fill('grey')
     level.run()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)