
import pygame
pygame.mixer.init()


GAME_MUSIC = "sounds/mysterious_music_level.wav"

MIOU_CAT_SOUND_FX = "sounds/cat.wav"

BAT_IMPACT_SOUND_FX = "sounds/bat_impact.wav"

SATAR_SOUND_FX = "sounds/coin_sound.wav"

PLAYER_DEATH_SOUND_FX = "sounds/player_death.wav"

ITEM_SOUND_FX = "sounds/item_sound.wav"

DOOR_OPEN_FX = "sounds/door_open_and_close.wav"

JUMP_FX = "sounds/player_jumping.wav"

GAME_OVER_FX = "sounds/arcade_game_over.wav"

WIN_GAME = "sounds/video_game_win.wav"



win_game = pygame.mixer.Sound(WIN_GAME)
win_game.set_volume(0.5)

game_over_fx = pygame.mixer.Sound(GAME_OVER_FX)
game_over_fx.set_volume(0.1)

game_music = pygame.mixer.music.load(GAME_MUSIC)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

miau_cat_sound = pygame.mixer.Sound(MIOU_CAT_SOUND_FX)
miau_cat_sound.set_volume(0.3)

star_coin_sound = pygame.mixer.Sound(SATAR_SOUND_FX)
star_coin_sound.set_volume(0.3)

bat_collision_sound = pygame.mixer.Sound(BAT_IMPACT_SOUND_FX)
bat_collision_sound.set_volume(0.3)

player_death_sound = pygame.mixer.Sound(BAT_IMPACT_SOUND_FX)
player_death_sound.set_volume(0.5)

key_sound = pygame.mixer.Sound(ITEM_SOUND_FX)
key_sound.set_volume(1)

door_open_sound = pygame.mixer.Sound(DOOR_OPEN_FX)
door_open_sound.set_volume(0.2)

jumping = pygame.mixer.Sound(JUMP_FX)
jumping.set_volume(0.3)



