
import pygame
pygame.mixer.init()


MIOU_CAT_SOUND = "sounds/cat.wav"

BAT_IMPACT_SOUND = "sounds/bat_impact.wav"

SATAR_SOUND = "sounds/coin_sound.wav"

PLAYER_DEATH_SOUND = "sounds/player_death.wav"

ITEM_SOUND = "sounds/item_sound.wav"

DOOR_OPEN = "sounds/door_open_and_close.wav"

miau_cat_sound = pygame.mixer.Sound(MIOU_CAT_SOUND)
miau_cat_sound.set_volume(0.10)

star_coin_sound = pygame.mixer.Sound(SATAR_SOUND)
star_coin_sound.set_volume(0.15)

bat_collision_sound = pygame.mixer.Sound(BAT_IMPACT_SOUND)
bat_collision_sound.set_volume(0.15)

player_death_sound = pygame.mixer.Sound(BAT_IMPACT_SOUND)
player_death_sound.set_volume(0.15)

key_sound = pygame.mixer.Sound(ITEM_SOUND)
key_sound.set_volume(.15)

door_open_sound = pygame.mixer.Sound(DOOR_OPEN)
door_open_sound.set_volume(0.2)




