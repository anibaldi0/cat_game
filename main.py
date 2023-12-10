import pygame
import sys
import csv

from constants import *
import random
from images import *
from sounds import *
from functions import *
# from maps import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("     Natacha's game")
icon = pygame.image.load(ICON_PATH)
pygame.display.set_icon(icon)

# player_name, previous_score_number = load_score()

# define variables
tile_size = 60
game_over = 0
level = 3
max_level = 3
main_menu = True
previous_score_number = 15
best_score_number = 10

miau_right_image = pygame.transform.scale(pygame.image.load(MIAU_SOUND_IMAGE).convert_alpha(), (WIDTH / 16, HEIGHT / 16))
miau_left_image = pygame.transform.flip(miau_right_image, True, False)

cat_death_image = pygame.transform.scale(pygame.image.load(CAT_DEATH_IMAGE).convert_alpha(), (WIDTH / 16, HEIGHT / 16))

background_normal_image = pygame.transform.scale(pygame.image.load(BACKGROUND_NORMAL_IMAGE).convert_alpha(), (WIDTH, HEIGHT))
background_exit_image = pygame.transform.scale(pygame.image.load(BACKGROUND_EXIT_IMAGE).convert_alpha(), (WIDTH, HEIGHT))
background_play_image = pygame.transform.scale(pygame.image.load(BACKGROUND_PLAY_IMAGE).convert_alpha(), (WIDTH, HEIGHT))
background_spider_web = pygame.transform.scale(pygame.image.load(BACKGROUND_SPIDER_WEB).convert_alpha(), (WIDTH, HEIGHT))


walk_right_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH // 20, HEIGHT // 16)) for image in PLAYER_WALK_RIGHT_IMAGES_LIST]
walk_left_images = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(image).convert_alpha(),
                        (WIDTH // 20, HEIGHT // 16)), True, False) for image in PLAYER_WALK_RIGHT_IMAGES_LIST]

ghost_cat_right_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH // 20, HEIGHT // 16)) for image in GHOST_PLAYER_WALK_RIGHT_IMAGES_LIST]
ghost_cat_left_images = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(image).convert_alpha(),
                        (WIDTH // 20, HEIGHT // 16)), True, False) for image in GHOST_PLAYER_WALK_RIGHT_IMAGES_LIST]

wall_image = pygame.transform.scale(pygame.image.load(WALL).convert_alpha(), (WIDTH / 18, HEIGHT / 18))
tree_image = pygame.transform.scale(pygame.image.load(TREE).convert_alpha(), (WIDTH / 16, HEIGHT / 11))

bat_left_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 17, HEIGHT / 17)) for image in BAT_LEFT_IMAGES_LIST]
bat_right_images = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(image).convert_alpha(), 
                        (WIDTH // 17, HEIGHT // 17)), True, False) for image in BAT_LEFT_IMAGES_LIST]

lava_fire_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 18, HEIGHT / 16)) for image in LAVA_FIRE_IMAGES_LIST]

lava_floor_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 18, HEIGHT / 16)) for image in LAVA_FLOOR_IMAGES_LIST]

ice_lava_floor_image = pygame.transform.scale(pygame.image.load(ICE_LAVA_FLOOR).convert_alpha(), (WIDTH / 18, HEIGHT / 12))

tree_right_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 12, HEIGHT / 8)) for image in TREE_IMAGES_LIST]
tree_left_images = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(image).convert_alpha(), 
                        (WIDTH // 12, HEIGHT // 8)), True, False) for image in TREE_IMAGES_LIST]

pumpkin_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 20, HEIGHT / 16)) for image in PUMPKIN_IMAGES_LIST]

fire_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 20, HEIGHT / 14)) for image in FIRE_IMAGES_LIST]

key_image = pygame.transform.scale(pygame.image.load(KEY).convert_alpha(), (WIDTH / 22, HEIGHT / 16))

star_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 24, HEIGHT / 20)) for image in STARS_LIST]

door_image = pygame.transform.scale(pygame.image.load(DOOR_IMAGE).convert_alpha(), (WIDTH / 22, HEIGHT / 16))

spell_book_image = pygame.transform.scale(pygame.image.load(BOOK_ITEM_IMAGE).convert_alpha(), (WIDTH / 18, HEIGHT / 14))

ice_right_platform_image = pygame.transform.scale(pygame.image.load(ICE_RIGHT_PLATFORM).convert_alpha(), (WIDTH / 18, HEIGHT / 13))

ice_block_image = pygame.transform.scale(pygame.image.load(ICE_BLOCK).convert_alpha(), (WIDTH / 18, HEIGHT / 13))

ice_left_platform_image = pygame.transform.scale(pygame.image.load(ICE_LEFT_PLATFORM).convert_alpha(), (WIDTH / 18, HEIGHT / 13))

ice_middle_floor_image = pygame.transform.scale(pygame.image.load(ICE_MIDDLE_FLOOR).convert_alpha(), (WIDTH / 18, HEIGHT / 13))

ice_platform_image = pygame.transform.scale(pygame.image.load(ICE_MIDDLE_FLOOR).convert_alpha(), (WIDTH / 18, HEIGHT / 20))

water_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 18, HEIGHT / 10)) for image in WATER_IMAGES_LIST]

start_normal_button_image = pygame.transform.scale(pygame.image.load(START_NORMAL_BUTTON_IMAGE).convert_alpha(), (WIDTH / 8, HEIGHT / 14))
start_hover_button_image = pygame.transform.scale(pygame.image.load(START_HOVER_BUTTON_IMAGE).convert_alpha(), (WIDTH / 8, HEIGHT / 14))

play_normal_button_image = pygame.transform.scale(pygame.image.load(PLAY_NORMAL_BUTTON_IMAGE).convert_alpha(), (WIDTH / 8, HEIGHT / 18))
play_hover_button_image = pygame.transform.scale(pygame.image.load(PLAY_HOVER_BUTTON_IMAGE).convert_alpha(), (WIDTH / 8, HEIGHT / 18))

exit_normal_button_image = pygame.transform.scale(pygame.image.load(EXIT_NORMAL_BUTTON_IMAGE).convert_alpha(), (WIDTH / 8, HEIGHT / 18))
exit_hover_button_image = pygame.transform.scale(pygame.image.load(EXIT_HOVER_BUTTON_IMAGE).convert_alpha(), (WIDTH / 8, HEIGHT / 18))

rip_cat = pygame.transform.scale(pygame.image.load(RIP_CAT).convert_alpha(), (WIDTH / 16, HEIGHT / 16))

game_over_font = pygame.font.Font(None, 80)



class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, normal_image, hover_image) -> None:
        self.normal_image = normal_image
        self.hover_image = hover_image
        self.image = normal_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        # self.label = label

    def draw(self, screen):
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.hover_image
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                print("press")
                action = True
                # self.image = start_button_pressed_image
                self.clicked = True
        else:
            self.image = self.normal_image

        if pygame.mouse.get_pressed()[0] == 0:
            # self.image = start_button_image
            self.clicked = False
        
        screen.blit(self.image, self.rect)
        return action


# Definir la clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.restart(x, y)

    def update(self, game_over):
        col_thresh = 50
        dx = 0
        dy = 0

        if game_over == 0:
            # Obtener las teclas presionadas
            keys = pygame.key.get_pressed()
            # Animación de caminar hacia la derecha
            if keys[pygame.K_d]:
                self.direction = 1
                dx += PLAYER_SPEED
                self.image = self.walk_images_right[self.walk_index // 5]  # Ajusta el divisor según la velocidad deseada de la animación
                self.walk_index += 1
                if self.walk_index >= len(self.walk_images_right) * 5:
                    self.walk_index = 0

            if keys[pygame.K_d] and self.spell_book == 1:
                self.direction = 1
                dx += PLAYER_SPEED
                self.image = self.ghost_right_images[self.walk_index // 5]  # Ajusta el divisor según la velocidad deseada de la animación
                self.walk_index += 1
                if self.walk_index >= len(self.ghost_right_images) * 5:
                    self.walk_index = 0

            # Animación de caminar hacia la izquierda
            if keys[pygame.K_a]:
                self.direction = -1
                dx -= PLAYER_SPEED
                self.image = self.walk_images_left[self.walk_index // 5]
                self.walk_index += 1
                if self.walk_index >= len(self.walk_images_left) * 5:
                    self.walk_index = 0

            if keys[pygame.K_a] and self.spell_book == 1:
                self.direction = -1
                dx -= PLAYER_SPEED
                self.image = self.ghost_left_images[self.walk_index // 5]
                self.walk_index += 1
                if self.walk_index >= len(self.ghost_left_images) * 5:
                    self.walk_index = 0

            if keys[pygame.K_a] == False and keys[pygame.K_d] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.walk_images_right[self.index]
                if self.direction == -1:
                    self.image = self.walk_images_left[self.index]

            if keys[pygame.K_a] == False and keys[pygame.K_d] == False and self.spell_book == 1:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.ghost_right_images[self.index]
                if self.direction == -1:
                    self.image = self.ghost_left_images[self.index]

            # Controlar el salto
            if keys[pygame.K_SPACE] and self.is_jumping == False and self.jump_count < self.max_jump_count:
                jumping.play()
                self.vel_y = -12
                self.is_jumping = True
                self.jump_count += 1

            if keys[pygame.K_SPACE] == False:
                self.is_jumping = False

            # Aplicar gravedad si el jugador está en el aire
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # comprobar colision con límites del mundo
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    self.jump_count = 0  # Restablecer jump_count cuando colisiona con el suelo
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Verificar si el jugador está subiendo o bajando
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.is_jumping = False
                        self.jump_count = 0  # Restablecer jump_count cuando colisiona con el suelo
            
            # Verificar colisiones con plataforma
            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.is_jumping = False
                        self.jump_count = 0
                        dy = 0
                    if platform.move_x == 1:
                        self.rect.x += platform.move_direction * 3
                    else:
                        self.rect.x += platform.move_direction * -1 * 3

            # Verificar colisiones con enemigos
            bat_hit = pygame.sprite.spritecollide(player, bat_group, False)
            for bat in bat_hit:
                if player.rect.colliderect(bat.rect):
                    player_death_sound.play()
                    player.lives -= 1
                    self.score_number -= 1
                    game_over = -1
                    print(player.lives)
                    self.spell_book = 0
            if player.rect.y < 0:
                player.rect.x = 10
                player.rect.y = 200

            tree_hit = pygame.sprite.spritecollide(player, tree_group, False)
            for tree in tree_hit:
                if player.rect.colliderect(tree.rect):
                    player_death_sound.play()
                    player.lives -= 1
                    self.score_number -= 1
                    game_over = -1
                    print(player.lives)
                    self.spell_book = 0
            if player.rect.y < 0:
                player.rect.x = 10
                player.rect.y = 200
                    
            # Verificar colisiones con estrellas
            stars_hit = pygame.sprite.spritecollide(self, stars_group, True)
            if stars_hit:
                star_coin_sound.play()
                self.score_number += 5
                print("Puntuación:", self.score_number)

            pumpkin_hit = pygame.sprite.spritecollide(self, pumpkin_group, True)
            if pumpkin_hit:
                if self.spell_book == 1:
                    star_coin_sound.play()
                    self.score_number += 5
                    print("Puntuación:", self.score_number)
                else:
                    player_death_sound.play()
                    player.lives -= 1
                    self.score_number -= 5
                    game_over = -1

            key_hit = pygame.sprite.spritecollide(self, key_group, True)
            if key_hit:
                key_sound.play()
                self.key_score += 1
                self.score_number += 10
                print("Llaves: {0}".format(self.key_score))

            spell_book_hit = pygame.sprite.spritecollide(self, spell_book_group, True)
            if spell_book_hit:
                key_sound.play()
                self.spell_book += 1
                self.score_number += 10
                print("Llaves: {0}".format(self.key_score))

            fire_hit = pygame.sprite.spritecollide(self, fire_group, False)
            if fire_hit:
                player_death_sound.play()
                player.lives -= 1
                self.score_number -= 1
                game_over = -1
                self.spell_book = 0

            water_hit = pygame.sprite.spritecollide(self, water_group, False)
            if water_hit:
                player_death_sound.play()
                player.lives -= 1
                self.score_number -= 1
                game_over = -1
                self.spell_book = 0

            lava_fire_hit = pygame.sprite.spritecollide(self, lava_fire_group, False)
            if lava_fire_hit:
                    player_death_sound.play()
                    player.lives -= 1
                    self.score_number -= 1
                    game_over = -1
                    self.spell_book = 0
                
            exit_hit = pygame.sprite.spritecollide(self, exit_group, False)
            if exit_hit:
                if self.key_score > 0:
                    door_open_sound.play()
                    game_over = 1
                    if level >= max_level:
                        win_game.play()
                else:
                    player_death_sound.play()
                    player.lives -= 1
                    self.score_number -= 2
                    game_over = -1
                    self.spell_book = 0

            lava_floor_hit = pygame.sprite.spritecollide(self, lava_floor_group, False)
            for lava in lava_floor_hit:
                if self.spell_book == 1:
                    print(self.spell_book)
                    # Ajustar la posición del jugador y reiniciar el salto
                    self.rect.y = lava.rect.top - self.height
                    self.is_jumping = False
                    self.jump_count = 0
                else:
                    player_death_sound.play()
                    player.lives -= 1
                    self.score_number -= 1
                    game_over = -1

            #coordenadas de player
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.x >= WIDTH - 60:
                self.rect.x = WIDTH - 60
            if self.rect.x <= 0:
                self.rect.x = 0
            if self.rect.y >= HEIGHT - 60:
                self.rect.y = HEIGHT - 60
            if self.rect.y <= 0:
                self.rect.y = 0
                    
        elif game_over == -1:
            self.image = cat_death_image
            self.rect.y -= 5
            if self.rect.y < -80:
                game_over = 0
            if self.lives <= 0:
                pygame.mixer.music.stop()
                game_over_fx.play()
                print("dead player")
                print("keys: {0}".format(self.key_score))
                print("lives: {0}".format(self.lives))
                print("score: {0}".format(self.score_number))
                if player.score_number >= previous_score_number:
                    best_score_number = player.score_number
                    print("jugador score {0}".format(player.score_number))
                    print("mejor score {0}".format(best_score_number))
                else:
                    best_score_number = previous_score_number
                    print("first player score {0}".format(player.score_number))
                    print("first Best score {0}".format(best_score_number))
                return
        return game_over
    
    def restart(self, x, y):
        self.can_shoot = False
        # Nuevas propiedades para la animación de caminar
        self.walk_index = 0
        self.walk_images_right = walk_right_images
        self.walk_images_left = walk_left_images
        self.ghost_right_images = ghost_cat_right_images
        self.ghost_left_images = ghost_cat_left_images

        self.image = self.walk_images_right[0] #el juego empieza con player a la derecha
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED
        self.vel_y = 0
        # self.jump_height = 15
        self.is_jumping = False
        self.jump_count = 10  # Inicializar jump_count aquí
        self.direction = 1
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.player_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.player_hitbox.fill(GREEN)
        self.player_hitbox_rect = self.player_hitbox.get_rect()  # Agregar esta línea
        # Nueva variable para rastrear la cantidad de saltos realizados
        self.jump_count = 0
        self.max_jump_count = 2  # Establece el límite de saltos consecutivos
        self.score_number = 0
        self.healt = 500
        self.lives = 3
        self.key_score = 0
        self.spell_book = 0
    
    def shoot(self, direction):
        if not self.can_shoot:
            if direction == 1:
                miau = Miau(self.rect.right, self.rect.centery - 25, self.direction)
            else:
                miau = Miau(self.rect.left - 50, self.rect.centery - 25, self.direction)
            miau_cat_sound.play()
            all_sprites.add(miau)
            miaus.add(miau)


class World():
    def __init__(self, data) -> None:
        self.restart(data)
            
    def restart(self, data):
        self.tile_list = []
        #load images
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 4:
                    img = wall_image
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 15:
                    img = tree_image
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 7:
                    img = ice_middle_floor_image
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 11:
                    img = ice_block_image
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 8:
                    img = ice_left_platform_image
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 13:
                    img = ice_right_platform_image
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 21:
                    platform = Platform(col_count * tile_size, row_count * tile_size + 35, 1, 10)
                    platform_group.add(platform)
                if tile == 10:
                    platform = Platform(col_count * tile_size, row_count * tile_size + 35, -1, 6)
                    platform_group.add(platform)
                if tile == 3:
                    tree = Tree(col_count * tile_size - 60, row_count * tile_size - 15, 4)
                    tree_group.add(tree)
                if tile == 14:
                    spell_book = SpellBook(col_count * tile_size, row_count * tile_size - 10)
                    spell_book_group.add(spell_book)
                if tile == 9:
                    water = Water(col_count * tile_size, row_count * tile_size + 15)
                    water_group.add(water)
                if tile == 0:
                    lava_floor = LavaFloor(col_count * tile_size, row_count * tile_size + 10)
                    lava_floor_group.add(lava_floor)
                if tile == 20:
                    pumpkin = Pumpkin(col_count * tile_size, row_count * tile_size)
                    pumpkin_group.add(pumpkin)
                if tile == 5:
                    door = Exit(col_count * tile_size + 10, row_count * tile_size + 20)
                    exit_group.add(door)
                if tile == 19:
                    key = Key(col_count * tile_size, row_count * tile_size + 5)
                    key_group.add(key)
                if tile == 16:
                    bat = Bat(col_count * tile_size, row_count * tile_size, random.choice([-1, 1]) * BAT_SPEED)
                    bat_group.add(bat)
                if tile == 2:
                    lava = LavaFire(col_count * tile_size, row_count * tile_size)
                    lava_fire_group.add(lava)
                if tile == 6:
                    fire = Fire(col_count * tile_size, row_count + 9.75 * tile_size, FIRE_SPEED)
                    fire_group.add(fire)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, RED, tile[1], 2)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, speed) -> None:
        super().__init__()
        self.image = ice_platform_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.move_couter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.ice_platform_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.ice_platform_hitbox.fill(WHITE)
        self.ice_platform_hitbox_rect = self.ice_platform_hitbox.get_rect()  # Agregar esta línea

    def update(self):
        # Lógica de actualización del enemigo (si es necesario)
        # Lógica de actualización del bat (movimiento por el eje x)
        self.rect.x += self.move_direction * self.move_x * 3
        self.move_couter += 1
        if abs(self.move_couter) > 80:
            self.move_direction *= -1
            self.move_couter *= -1

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = key_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 5 # Ajustar la posición vertical según sea necesario
        self.key_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.key_hitbox.fill(RED)
        self.key_hitbox_rect = self.key_hitbox.get_rect()

    def update(self):
        # Actualizar la posición de la hitbox de la llave
        self.key_hitbox_rect.topleft = self.rect.topleft
        # Renderizar la hitbox de la llave
        screen.blit(self.key_hitbox, self.key_hitbox_rect)

class SpellBook(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = spell_book_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 10  # Ajustar la posición vertical según sea necesario
        self.spell_book_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.spell_book_hitbox.fill(RED)
        self.spell_book_hitbox_rect = self.spell_book_hitbox.get_rect()

    def update(self):
        # Actualizar la posición de la hitbox de la llave
        self.spell_book_hitbox_rect.topleft = self.rect.topleft
        # Renderizar la hitbox de la llave
        screen.blit(self.spell_book_hitbox, self.spell_book_hitbox_rect)

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = door_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 8 # Ajustar la posición vertical según sea necesario
        self.exit_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.exit_hitbox.fill(RED)
        self.exit_hitbox_rect = self.exit_hitbox.get_rect()

    def update(self):
        # Actualizar la posición de la hitbox de la llave
        self.exit_hitbox_rect.topleft = self.rect.topleft
        # Renderizar la hitbox de la llave
        screen.blit(self.exit_hitbox, self.exit_hitbox_rect)

class Pumpkin(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.pumpkin_index = 0
        self.pumpkin_images = pumpkin_images
        self.image = pumpkin_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 15# Ajustar la posición vertical según sea necesario
        self.pumpkin_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.pumpkin_hitbox.fill(RED)
        self.pumpkin_hitbox_rect = self.pumpkin_hitbox.get_rect()

    def update(self):
        # Actualizar la posición de la hitbox de la estrella
        # self.lava_hitbox.topleft = self.rect.topleft

        # Cambiar la imagen de la estrella según el índice
        self.image = self.pumpkin_images[self.pumpkin_index // 10]

        # Incrementar el índice para cambiar la imagen en el próximo ciclo
        self.pumpkin_index += 1
        if self.pumpkin_index >= len(self.pumpkin_images) * 10:
            self.pumpkin_index = 0
        screen.blit(self.pumpkin_hitbox, self.pumpkin_hitbox_rect)

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.water_index = 0
        self.water_images = water_images
        self.image = water_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y # Ajustar la posición vertical según sea necesario
        self.water_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.water_hitbox.fill(RED)
        self.water_hitbox_rect = self.water_hitbox.get_rect()

    def update(self):
        # Actualizar la posición de la hitbox de la estrella
        # self.lava_hitbox.topleft = self.rect.topleft

        # Cambiar la imagen de la estrella según el índice
        self.image = self.water_images[self.water_index // 10]

        # Incrementar el índice para cambiar la imagen en el próximo ciclo
        self.water_index += 1
        if self.water_index >= len(self.water_images) * 10:
            self.water_index = 0
        screen.blit(self.water_hitbox, self.water_hitbox_rect)

class LavaFloor(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.lava_floor_index = 0
        self.lava_floor_images = lava_floor_images
        self.image = lava_floor_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y # Ajustar la posición vertical según sea necesario
        self.lava_floor_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.lava_floor_hitbox.fill(RED)
        self.lava_floor_hitbox_rect = self.lava_floor_hitbox.get_rect()

    def update(self):
        # Actualizar la posición de la hitbox de la estrella
        # self.lava_hitbox.topleft = self.rect.topleft

        # Cambiar la imagen de la estrella según el índice
        
        self.image = self.lava_floor_images[self.lava_floor_index // 10]

        # Incrementar el índice para cambiar la imagen en el próximo ciclo
        self.lava_floor_index += 1
        if self.lava_floor_index >= len(self.lava_floor_images) * 10:
            self.lava_floor_index = 0
        screen.blit(self.lava_floor_hitbox, self.lava_floor_hitbox_rect)

class LavaFire(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.lava_fire_index = 0
        self.lava_fire_images = lava_fire_images
        self.image = lava_fire_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y # Ajustar la posición vertical según sea necesario
        self.lava_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.lava_hitbox.fill(RED)
        self.lava_hitbox = self.lava_hitbox.get_rect()

    def update(self):
        # Actualizar la posición de la hitbox de la estrella
        # self.lava_hitbox.topleft = self.rect.topleft

        # Cambiar la imagen de la estrella según el índice
        self.image = self.lava_fire_images[self.lava_fire_index // 10]

        # Incrementar el índice para cambiar la imagen en el próximo ciclo
        self.lava_fire_index += 1
        if self.lava_fire_index >= len(self.lava_fire_images) * 10:
            self.lava_fire_index = 0

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        super().__init__()
        self.fire_index = 0
        self.fire_images = fire_images
        self.image = fire_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.move_couter = 0
        self.direction = 0
        self.fire_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.fire_hitbox.fill(WHITE)
        self.fire_hitbox_rect = self.fire_hitbox.get_rect()  # Agregar esta línea

    def update(self):
        # Lógica de actualización del enemigo (si es necesario)

        self.rect.y -= 2
        if self.rect.y == 500:
            self.rect.y = 780

        self.fire_index += 1
        if self.fire_index >= len(self.fire_images) * 10:
            self.fire_index = 0

        # Cambiar la imagen de la estrella según el índice
        self.image = self.fire_images[self.fire_index // 10]


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.star_index = 0
        self.star_images = star_images
        self.image = star_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 20

        # Crear la hitbox de la estrella (rectángulo rojo)
        self.star_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.star_hitbox.fill(RED)
        self.star_hitbox_rect = self.star_hitbox.get_rect()

    def update(self):
        # Actualizar la posición de la hitbox de la estrella
        self.star_hitbox_rect.topleft = self.rect.topleft

        # Cambiar la imagen de la estrella según el índice
        self.image = self.star_images[self.star_index // 10]

        # Incrementar el índice para cambiar la imagen en el próximo ciclo
        self.star_index += 1
        if self.star_index >= len(self.star_images) * 10:
            self.star_index = 0

        # Renderizar la hitbox de la estrella
        screen.blit(self.star_hitbox, self.star_hitbox_rect)

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        super().__init__()
        self.tree_index = 0
        self.tree_left_images = tree_left_images
        self.tree_right_images = tree_right_images
        self.image = tree_left_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = TREE_SPEED
        self.move_couter = 0
        self.direction = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.tree_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.tree_hitbox.fill(GREEN)
        self.tree_hitbox_rect = self.tree_hitbox.get_rect()  # Agregar esta línea
        # self.player_hitbox = self.bat_hitbox.get_rect()  # Agregar esta línea

    def update(self):
        # Lógica de actualización del bat (movimiento por el eje x)
        self.rect.x += self.speed
        self.move_couter += 1
        if abs(self.move_couter) > 40:
            self.speed *= -1
            self.move_couter *= -1

                # Cambiar la imagen del murciélago según la dirección
        if self.speed > 0:  # Si el murciélago se mueve hacia la derecha
            self.image = self.tree_left_images[self.tree_index // 5]
            
        else:  # Si el murciélago se mueve hacia la izquierda
            self.image = self.tree_right_images[self.tree_index // 5]

        self.tree_index += 1
        if self.tree_index >= len(self.tree_left_images) * 5:
            self.tree_index = 0

class Bat(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        super().__init__()
        self.bat_index = 0
        self.bat_left_images = bat_left_images
        self.bat_right_images = bat_right_images
        self.image = bat_left_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.move_couter = 0
        self.direction = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.bat_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.bat_hitbox.fill(GREEN)
        self.bat_hitbox_rect = self.bat_hitbox.get_rect()  # Agregar esta línea
        # self.player_hitbox = self.bat_hitbox.get_rect()  # Agregar esta línea

    def update(self):
        # Lógica de actualización del bat (movimiento por el eje x)
        self.rect.x += self.speed
        self.move_couter += 1
        if abs(self.move_couter) > 60:
            self.speed *= -1
            self.move_couter *= -1

                # Cambiar la imagen del murciélago según la dirección
        if self.speed > 0:  # Si el murciélago se mueve hacia la derecha
            self.image = self.bat_right_images[self.bat_index // 5]
        else:  # Si el murciélago se mueve hacia la izquierda
            self.image = self.bat_left_images[self.bat_index // 5]

        self.bat_index += 1
        if self.bat_index >= len(self.bat_left_images) * 5:
            self.bat_index = 0


# Definir la clase Miau (proyectil)
class Miau(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        if direction == 1:
            self.image = miau_right_image
        else:
            self.image = miau_left_image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.speed = 6
        self.direction = direction
        # Crear la hitbox del proyectil (rectángulo rojo)
        self.hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.hitbox.fill(RED)
        self.miau_hitbox = self.hitbox.get_rect()

    def update(self):

        self.rect.x += self.direction * self.speed
        # Eliminar el proyectil si sale de la pantalla
        if self.rect.x < 0 or self.rect.x > WIDTH - 60:
            self.kill()
        # Actualizar la posición de la hitbox del proyectil
        self.miau_hitbox.topleft = self.rect.topleft

        # comprobar colision con límites del mundo
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                self.kill()

        # Verificar colisiones con enemigos
        enemies_hit = pygame.sprite.spritecollide(self, bat_group, True)
        for enemy in enemies_hit:
            # Aquí puedes agregar lógica adicional si es necesario
            # por ejemplo, eliminar el proyectil y reducir la vida del enemigo
            bat_collision_sound.play()
            self.kill()
            player.score_number += 5
            star = Star(enemy.rect.x, enemy.rect.y)
            # all_sprites.add(star)
            stars_group.add(star)

        tree_hit = pygame.sprite.spritecollide(self, tree_group, False)
        for tree in tree_hit:
            # Aquí puedes agregar lógica adicional si es necesario
            # por ejemplo, eliminar el proyectil y reducir la vida del enemigo
            # bat_collision_sound.play()
            self.kill()
            # player.score_number += 5
            # star = Star(tree.rect.x, tree.rect.y - 25)
            # # all_sprites.add(star)
            # stars_group.add(star)

def empty_groups():
    platform_group.empty()
    spell_book_group.empty()
    water_group.empty()
    lava_floor_group.empty()
    tree_group.empty()
    pumpkin_group.empty()
    bat_group.empty()
    key_group.empty()
    stars_group.empty()
    fire_group.empty()
    lava_fire_group.empty()
    exit_group.empty()

world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

with open("level{0}_data.csv".format(level), newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
print(world_data)

# Crear jugador
player = Player(x=10, y= 200)
platform_group = pygame.sprite.Group()
spell_book_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
lava_floor_group = pygame.sprite.Group()
pumpkin_group = pygame.sprite.Group()
tree_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
lava_fire_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
bat_group = pygame.sprite.Group()
world = World(world_data)
stars_group = pygame.sprite.Group()
start_button = Button(WIDTH / 2 - 50, HEIGHT / 2 + 100, start_normal_button_image, start_hover_button_image)
play_button = Button(WIDTH / 2 - 360, HEIGHT / 2 + 250, play_normal_button_image, play_hover_button_image)
exit_button = Button(WIDTH / 2 + 250, HEIGHT / 2 + 250, exit_normal_button_image, exit_hover_button_image)

# Crear grupo de sprites y agregar el jugador al grupo
miaus = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

playing_music = True
text = ""
font_size = 60
font = pygame.font.Font(None, font_size)
def darw_player_input(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    width = img.get_width()
    text = ""
    screen.blit(img, (x - (width / 2), y))
    return text

wolves_intro.play()
mute_key = pygame.K_m
is_muted = False
volume_up_key = pygame.K_l
volume_down_key = pygame.K_k

# Bucle principal del juego
running = True
while running:

    game_over = player.update(game_over)
    # Manejo de eventos
    for event in pygame.event.get():
        # handle text input
        if event.type == pygame.TEXTINPUT:
            text += event.text

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not player.can_shoot:
                player.shoot(player.direction)
                player.can_shoot = True
            else:
                player.can_shoot = False

            if event.key == pygame.K_p:
                if playing_music:
                    pygame.mixer.music.pause()
                show_paused_text(screen, "PAUSED", game_over_font, (WIDTH / 2, HEIGHT / 2), RED)
                wait_user()
                if playing_music:
                    pygame.mixer.music.unpause()

            if event.key == mute_key:
                is_muted = not is_muted
                if is_muted:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            if event.key == volume_up_key:
                current_volume = min(1.0, current_volume + 0.1)
                wolves_intro.set_volume(current_volume)
                win_game.set_volume(current_volume)
                game_over_fx.set_volume(current_volume)
                miau_cat_sound.set_volume(current_volume)
                star_coin_sound.set_volume(current_volume)
                bat_collision_sound.set_volume(current_volume)
                player_death_sound.set_volume(current_volume)
                key_sound.set_volume(current_volume)
                door_open_sound.set_volume(current_volume)
                jumping.set_volume(current_volume)
            elif event.key == volume_down_key:
                current_volume = max(0.0, current_volume - 0.1)
                wolves_intro.set_volume(current_volume)
                win_game.set_volume(current_volume)
                game_over_fx.set_volume(current_volume)
                miau_cat_sound.set_volume(current_volume)
                star_coin_sound.set_volume(current_volume)
                bat_collision_sound.set_volume(current_volume)
                player_death_sound.set_volume(current_volume)
                key_sound.set_volume(current_volume)
                door_open_sound.set_volume(current_volume)
                jumping.set_volume(current_volume)
        

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.direction = -1  # Si se suelta K_a, la direccion continua a la izquierda
            elif event.key == pygame.K_d:
                player.direction = 1

    if main_menu == True:
        # Verificar si el cursor está sobre el botón play_button
        if play_button.rect.collidepoint(pygame.mouse.get_pos()):
            # Cambiar la imagen del fondo cuando el cursor está sobre play_button
            background_image = background_play_image
        elif exit_button.rect.collidepoint(pygame.mouse.get_pos()):
            # Restablecer la imagen del fondo al estado normal
            background_image = background_exit_image
        else:
            background_image = background_normal_image

        # Dibujar el fondo en la pantalla
        screen.blit(background_image, (0, 0))

        if play_button.draw(screen):
            print("Play button pressed")
            pygame.mixer.music.play(-1)
            main_menu = False

        if exit_button.draw(screen):
            print("Exit button pressed")
            running = False
    else:
        # best_score_number = previous_score_number
        print("best {0} y score {1}".format(best_score_number, player.score_number))
        if player.score_number >= best_score_number:
            best_score_number = player.score_number
            print("player score {0}".format(player.score_number))
            print("Best score {0}".format(best_score_number))
        else:
            best_score_number = previous_score_number
            print("second player score {0}".format(player.score_number))
            print("second Best score {0}".format(best_score_number))
        # save_score(player_name, best_score_number)
        # Actualizar
        platform_group.update()
        spell_book_group.update()
        water_group.update()
        lava_floor_group.update()
        tree_group.update()
        pumpkin_group.update()
        exit_group.update()
        fire_group.update()
        lava_fire_group.update()
        key_group.update()
        bat_group.update()
        all_sprites.update()
        stars_group.update()

        # Dibujar en la pantalla
        screen.blit(background_spider_web, (0, 0))
        # screen.fill(BLACK)
        
        screen.blit(player.image, player.rect)
        world.draw()
        # play_button.draw(screen)
        # exit_button.draw(screen)
        key_group.draw(screen)
        platform_group.draw(screen)
        spell_book_group.draw(screen)
        water_group.draw(screen)
        lava_floor_group.draw(screen)
        tree_group.draw(screen)
        pumpkin_group.draw(screen)
        exit_group.draw(screen)
        fire_group.draw(screen)
        lava_fire_group.draw(screen)
        # key_group.draw(screen)
        bat_group.draw(screen)
        stars_group.draw(screen)
        all_sprites.draw(screen)

                    # Dibujar información en la pantalla (Score, Lives, Keys)
        font = pygame.font.Font(None, 36)  # Puedes ajustar el tamaño de la fuente según tus preferencias

        spell_book_score = font.render("Spell Book: {0}".format(player.spell_book), True, GOLD)
        screen.blit(spell_book_score, (450, 10))

        # Renderizar texto para Score
        score_text = font.render("Score: {0}".format(player.score_number), True, GOLD)
        screen.blit(score_text, (150, 10))

        # Renderizar texto para Lives
        lives_text = font.render("Lives: {0}".format(int(player.lives)), True, GOLD)
        screen.blit(lives_text, (300, 10))

        # Renderizar texto para Keys
        keys_text = font.render("Keys: {0}".format(player.key_score), True, GOLD)
        screen.blit(keys_text, (650, 10))

        # Renderizar texto para Keys
        best_score_text = font.render("Best score: {0}".format(best_score_number), True, BLUE)
        screen.blit(best_score_text, (820, 10))
        print("mejor numero {0}".format(best_score_number))

        if game_over == -1:
            if player.key_score >= 1:
                player.key_score = 0
                player.score_number -= 10
                if player.score_number < 0:
                    player.score_number = 0
            if player.rect.y < 0:
                for _ in range(1):
                    key_group.empty()
                    nueva_llave = Key(1020, 605)  # Ajusta las coordenadas (x, y) según tus necesidades
                    key_group.add(nueva_llave)

        if player.lives <= 0:

            player.image = rip_cat
            player.rect.y += 1
            for tile in world.tile_list:
                if tile[1].colliderect(player.rect.x, player.rect.y, player.width, player.height):
                    # El jugador ha colisionado con un tile, detén el movimiento hacia abajo
                    player.rect.y = tile[1].top - player.height
                    break

            game_over_text = game_over_font.render("Game Over", True, RED)
            game_over_text_rect = game_over_text.get_rect()
            game_over_text_rect.center = (WIDTH / 2, HEIGHT / 2)
            screen.blit(game_over_text, game_over_text_rect)

            print_player_score = game_over_font.render("Score {0}".format(player.score_number), True, YELLOW)
            print_player_score_rect = print_player_score.get_rect()
            print_player_score_rect.center = (WIDTH / 2, HEIGHT / 3)
            screen.blit(print_player_score, print_player_score_rect)

            pygame.mixer.music.stop()

            # if tile[1].colliderect(player.rect.x, player.rect.y, player.width, player.height):
            #         # El jugador ha colisionado con un tile, detén el movimiento hacia abajo
            #         player.rect.y = tile[1].top - player.height 

            # show_paused_text(screen, "", game_over_font, (WIDTH / 2, HEIGHT / 2), RED)
            # wait_user()
            
            if play_button.draw(screen):
                print("Restart button pressed")
                pygame.mixer.music.play(-1)
                empty_groups()
                level = 1  # Reiniciar al nivel 1
                world_data = [[-1] * COLS for _ in range(ROWS)]
                with open("level1_data.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world.restart(world_data)
                player.restart(x=10, y=200)
                game_over = 0

            if exit_button.draw(screen):
                print("Exit button pressed")
                running = False
                
        if game_over == 1:
            print("cruza puerta")
            print("lives {0} y score {1}".format(player.lives, player.score_number))
            previous_lives = player.lives
            previous_score_number = player.score_number
            if player.score_number > previous_score_number:
                best_score_number = player.score_number
            print("previous lives {0} y previous score {1}".format(previous_lives, previous_score_number))
            level += 1
            empty_groups()
            if level <= max_level:
                world_data = [[-1] * COLS for _ in range(ROWS)]
                with open("level{0}_data.csv".format(level), newline="") as csvfile:
                    reader = csv.reader(csvfile, delimiter=",")
                    print("level{0}_data.csv".format(level))
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                world.restart(world_data)
                player.restart(x=10, y= 200)
                game_over = 0
                # player.score_number
                player.score_number = previous_score_number
                player.lives = previous_lives
                print("paso por level <= max_level")
                # print("best score {0}, score {1}, previous {2}".format(best_score_number, player.score_number, previous_score_number))
            else:
                previous_lives = player.lives
                if player.score_number > previous_score_number:
                    best_score_number = player.score_number
                print("best score {0}, score {1}, previous {2}".format(best_score_number, player.score_number, previous_score_number))
                screen.fill(BLACK)
                door_open_sound.stop()
                pygame.mixer.music.stop()
                game_over_text = game_over_font.render("You Win", True, WHITE)
                game_over_text_rect = game_over_text.get_rect()
                game_over_text_rect.center = (WIDTH / 2, HEIGHT / 2)
                screen.blit(game_over_text, game_over_text_rect)
                player.restart(x=-100, y=-100)
                print("paso por level > max_level")
                final_score = best_score_number
                print("final_score {0}".format(final_score))
                show_paused_text(screen, "", game_over_font, (WIDTH / 2, HEIGHT / 2), RED)
                wait_user()

        # screen.blit(player.image, player.rect)

    # #Dibujar hitbox
    # for miau in miaus:
    #     pygame.draw.rect(screen, RED, miau.rect, 2)

    # for fire in fire_group:
    #     pygame.draw.rect(screen, WHITE, fire.rect, 2)

    # for lava in lava_fire_group:
    #     pygame.draw.rect(screen, GRAY, lava.rect, 2)

    # for bat in bat_group:
    #     pygame.draw.rect(screen, ORANGE, bat.rect, 2)

    # #Dibujar hitbox del jugador
    # pygame.draw.rect(screen, GREEN, player.rect, 2)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    pygame.time.Clock().tick(FPS)

# Salir del juego
pygame.quit()
sys.exit()




