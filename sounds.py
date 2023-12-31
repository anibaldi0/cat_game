
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

WOLVES_INTRO = "sounds/wolves_intro.wav"

INITIAL_VOLUME = 0.5
current_volume = INITIAL_VOLUME

win_game = pygame.mixer.Sound(WIN_GAME)
win_game.set_volume(INITIAL_VOLUME - 0.2)

game_over_fx = pygame.mixer.Sound(GAME_OVER_FX)
game_over_fx.set_volume(INITIAL_VOLUME)

game_music = pygame.mixer.music.load(GAME_MUSIC)
pygame.mixer.music.set_volume(INITIAL_VOLUME)
# pygame.mixer.music.play(-1)

wolves_intro = pygame.mixer.Sound(WOLVES_INTRO)
wolves_intro.set_volume(INITIAL_VOLUME)

miau_cat_sound = pygame.mixer.Sound(MIOU_CAT_SOUND_FX)
miau_cat_sound.set_volume(INITIAL_VOLUME)

star_coin_sound = pygame.mixer.Sound(SATAR_SOUND_FX)
star_coin_sound.set_volume(INITIAL_VOLUME)

bat_collision_sound = pygame.mixer.Sound(BAT_IMPACT_SOUND_FX)
bat_collision_sound.set_volume(INITIAL_VOLUME)

player_death_sound = pygame.mixer.Sound(BAT_IMPACT_SOUND_FX)
player_death_sound.set_volume(INITIAL_VOLUME)

key_sound = pygame.mixer.Sound(ITEM_SOUND_FX)
key_sound.set_volume(INITIAL_VOLUME)

door_open_sound = pygame.mixer.Sound(DOOR_OPEN_FX)
door_open_sound.set_volume(INITIAL_VOLUME)

jumping = pygame.mixer.Sound(JUMP_FX)
jumping.set_volume(INITIAL_VOLUME)



