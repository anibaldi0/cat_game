import pygame
import sys
import csv

from constants import *
import random
from images import *
from sounds import *
# from maps import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("     Natacha's game")
icon = pygame.image.load(ICON_PATH)
pygame.display.set_icon(icon)

# define variables
tile_size = 80
game_over = 0
COLS = 16
ROWS = 12
level = 2
max_level = 3



miau_right_image = pygame.transform.scale(pygame.image.load(MIAU_SOUND_IMAGE).convert_alpha(), (WIDTH / 16, HEIGHT / 16))
miau_left_image = pygame.transform.flip(miau_right_image, True, False)

cat_death_image = pygame.transform.scale(pygame.image.load(CAT_DEATH_IMAGE).convert_alpha(), (WIDTH / 16, HEIGHT / 16))

walk_right_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH // 20, HEIGHT // 16)) for image in PLAYER_WALK_RIGHT_IMAGES_LIST]
walk_left_images = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(image).convert_alpha(),
                        (WIDTH // 20, HEIGHT // 16)), True, False) for image in PLAYER_WALK_RIGHT_IMAGES_LIST]

wall_image = pygame.transform.scale(pygame.image.load(WALL).convert_alpha(), (WIDTH / 16, HEIGHT / 17))
tree_image = pygame.transform.scale(pygame.image.load(TREE).convert_alpha(), (WIDTH / 16, HEIGHT / 11))

bat_left_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 17, HEIGHT / 17)) for image in BAT_LEFT_IMAGES_LIST]
bat_right_images = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(image).convert_alpha(), 
                        (WIDTH // 17, HEIGHT // 17)), True, False) for image in BAT_LEFT_IMAGES_LIST]

lava_fire_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 16, HEIGHT / 22)) for image in LAVA_FIRE_IMAGES_LIST]

lava_floor_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 16, HEIGHT / 14)) for image in LAVA_FLOOR_IMAGES_LIST]

worm_left_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 16, HEIGHT / 22)) for image in WORM_IMAGE_LIST]
worm_right_images = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(image).convert_alpha(), 
                        (WIDTH // 16, HEIGHT // 22)), True, False) for image in WORM_IMAGE_LIST]

pumpkin_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 20, HEIGHT / 16)) for image in PUMPKIN_IMAGE_LIST]

fire_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 20, HEIGHT / 10)) for image in FIRE_IMAGES_LIST]

key_image = pygame.transform.scale(pygame.image.load(KEY).convert_alpha(), (WIDTH / 22, HEIGHT / 16))

star_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 24, HEIGHT / 20)) for image in STARS_LIST]

door_image = pygame.transform.scale(pygame.image.load(DOOR_IMAGE).convert_alpha(), (WIDTH / 22, HEIGHT / 16))

spell_book_image = pygame.transform.scale(pygame.image.load(BOOK_ITEM_IMAGE).convert_alpha(), (WIDTH / 16, HEIGHT / 16))

ice_right_platform_image = pygame.transform.scale(pygame.image.load(ICE_RIGHT_PLATFORM).convert_alpha(), (WIDTH / 16, HEIGHT / 12))

ice_block_image = pygame.transform.scale(pygame.image.load(ICE_BLOCK).convert_alpha(), (WIDTH / 16, HEIGHT / 12))

ice_left_platform_image = pygame.transform.scale(pygame.image.load(ICE_LEFT_PLATFORM).convert_alpha(), (WIDTH / 16, HEIGHT / 12))

ice_middle_floor_image = pygame.transform.scale(pygame.image.load(ICE_MIDDLE_FLOOR).convert_alpha(), (WIDTH / 16, HEIGHT / 12))

ice_platform_image = pygame.transform.scale(pygame.image.load(ICE_MIDDLE_FLOOR).convert_alpha(), (WIDTH / 16, HEIGHT / 20))

water_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 16, HEIGHT / 10)) for image in WATER_IMAGES_LIST]

start_button_image = pygame.transform.scale(pygame.image.load(START_BUTTON_IMAGE).convert_alpha(), (WIDTH / 10, HEIGHT / 10))
start_button_pressed_image = pygame.transform.scale(pygame.image.load(START_BUTTON_PRESSED_IMAGE).convert_alpha(), (WIDTH / 10, HEIGHT / 10))

rip_cat = pygame.transform.scale(pygame.image.load(RIP_CAT).convert_alpha(), (WIDTH / 16, HEIGHT / 16))

game_over_font = pygame.font.Font(None, 80)

class Button():
    def __init__(self, x, y, image) -> None:
        self.image = start_button_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, screen):
        action = False
        
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                print("press")
                action = True
                self.image = start_button_pressed_image
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.image = start_button_image
            self.clicked = False
        
        screen.blit(self.image, self.rect)
        return action


# Definir la clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.restart(x, y)

    def update(self, game_over):
        col_thresh = 20
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

            # Animación de caminar hacia la izquierda
            if keys[pygame.K_a]:
                self.direction = -1
                dx -= PLAYER_SPEED
                self.image = self.walk_images_left[self.walk_index // 5]
                self.walk_index += 1
                if self.walk_index >= len(self.walk_images_left) * 5:
                    self.walk_index = 0

            if keys[pygame.K_a] == False and keys[pygame.K_d] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.walk_images_right[self.index]
                if self.direction == -1:
                    self.image = self.walk_images_left[self.index]

            # Controlar el salto
            if keys[pygame.K_SPACE] and self.is_jumping == False and self.jump_count < self.max_jump_count:
                jumping.play()
                self.vel_y = -15
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
                    self.score -= 1
                    self.rect.y -= 2
                    game_over = -1
                    print(player.lives)
            if player.rect.y < 0:
                player.rect.x = 200
                player.rect.y = 255

            worm_hit = pygame.sprite.spritecollide(player, worm_group, False)
            for worm in worm_hit:
                if player.rect.colliderect(worm.rect):
                    player_death_sound.play()
                    player.lives -= 1
                    self.score -= 1
                    self.rect.y -= 2
                    game_over = -1
                    print(player.lives)
            if player.rect.y < 0:
                player.rect.x = 200
                player.rect.y = 255
                    
            # Verificar colisiones con estrellas
            stars_hit = pygame.sprite.spritecollide(self, stars_group, True)
            for star in stars_hit:
                star_coin_sound.play()
                self.score += 5
                print("Puntuación:", self.score)

            pumpkin_hit = pygame.sprite.spritecollide(self, pumpkin_group, True)
            for pumpkin in pumpkin_hit:
                star_coin_sound.play()
                self.score += 5
                print("Puntuación:", self.score)

            key_hit = pygame.sprite.spritecollide(self, key_group, True)
            for key in key_hit:
                key_sound.play()
                self.key_score += 1
                self.score += 10
                print("Llaves: {0}".format(self.key_score))

            spell_book_hit = pygame.sprite.spritecollide(self, spell_book_group, True)
            for spell_book in spell_book_hit:
                key_sound.play()
                self.spell_book += 1
                self.score += 10
                print("Llaves: {0}".format(self.key_score))

            fire_hit = pygame.sprite.spritecollide(self, fire_group, False)
            for fire in fire_hit:
                player_death_sound.play()
                player.lives -= 1
                self.score -= 1
                game_over = -1
                player.image = cat_death_image
                self.rect.y -= 2

            water_hit = pygame.sprite.spritecollide(self, water_group, False)
            for water in water_hit:
                player_death_sound.play(1)
                player.lives -= 1
                self.score -= 1
                game_over = -1
                player.image = cat_death_image
                self.rect.y -= 2

            lava_fire_hit = pygame.sprite.spritecollide(self, lava_fire_group, False)
            for lava in lava_fire_hit:
                if self.spell_book == 1:
                    print(self.spell_book)
                    # Ajustar la posición del jugador y reiniciar el salto
                    self.rect.y = lava.rect.top - self.height
                    # self.vel_y = 0
                    self.is_jumping = False
                    self.jump_count = 0
                else:
                    player_death_sound.play(1)
                    player.lives -= 1
                    self.score -= 1
                    game_over = -1
                    player.image = cat_death_image
                    self.rect.y -= 2
                
            exit_hit = pygame.sprite.spritecollide(self, exit_group, False)
            for exit in exit_hit:
                if self.key_score > 0:
                    door_open_sound.play()
                    game_over = 1
                else:
                    player_death_sound.play()
                    player.lives -= 1
                    self.score -= 2
                    game_over = -1
                    player.image = cat_death_image
                    self.rect.y -= 2

            lava_floor_hit = pygame.sprite.spritecollide(self, lava_floor_group, False)
            for lava in lava_floor_hit:
                if self.spell_book == 1:
                    print(self.spell_book)
                    # Ajustar la posición del jugador y reiniciar el salto
                    self.rect.y = lava.rect.top - self.height
                    # self.vel_y = 0
                    self.is_jumping = False
                    self.jump_count = 0
                else:
                    player_death_sound.play(1)
                    player.lives -= 1
                    self.score -= 1
                    game_over = -1
                    player.image = cat_death_image
                    self.rect.y -= 2

                


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
                print("game over")
                print("keys: {0}".format(self.key_score))
                print("lives: {0}".format(self.lives))
                print("score: {0}".format(self.score))
                return 
        return game_over
    
    def restart(self, x, y):
        self.can_shoot = False
        # Nuevas propiedades para la animación de caminar
        self.walk_index = 0
        self.walk_images_right = walk_right_images
        self.walk_images_left = walk_left_images

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
        self.score = 0
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
                    worm = Worm(col_count * tile_size, row_count * tile_size + 35, 6)
                    worm_group.add(worm)
                if tile == 14:
                    spell_book = SpellBook(col_count * tile_size, row_count * tile_size)
                    spell_book_group.add(spell_book)
                if tile == 9:
                    water = Water(col_count * tile_size, row_count * tile_size)
                    water_group.add(water)
                if tile == 0:
                    lava_floor = LavaFloor(col_count * tile_size, row_count * tile_size + 10)
                    lava_floor_group.add(lava_floor)
                if tile == 20:
                    pumpkin = Pumpkin(col_count * tile_size, row_count * tile_size + 25)
                    fire_group.add(pumpkin)
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
                    fire = Fire(col_count * tile_size, row_count + 9.45 * tile_size, FIRE_SPEED)
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
        if abs(self.move_couter) > 120:
            self.move_direction *= -1
            self.move_couter *= -1

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = key_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + 15  # Ajustar la posición vertical según sea necesario
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
        self.rect.y = y + 15  # Ajustar la posición vertical según sea necesario
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
        self.rect.y = y  # Ajustar la posición vertical según sea necesario
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
        self.rect.y = y # Ajustar la posición vertical según sea necesario
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
        self.rect.y = y + 13 # Ajustar la posición vertical según sea necesario
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
        if self.rect.y == 600:
            self.rect.y = 950

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
        self.rect.y = y + 25

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

class Worm(pygame.sprite.Sprite):
    def __init__(self, x, y, speed) -> None:
        super().__init__()
        self.worm_index = 0
        self.worm_left_images = worm_left_images
        self.image = worm_left_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.move_couter = 0
        self.direction = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.worm_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.worm_hitbox.fill(GREEN)
        self.worm_hitbox_rect = self.worm_hitbox.get_rect()  # Agregar esta línea
        self.player_hitbox = self.worm_hitbox.get_rect()  # Agregar esta línea

    def update(self):
        # Lógica de actualización del bat (movimiento por el eje x)
        self.rect.x += self.speed
        self.move_couter += 1
        if abs(self.move_couter) > 50:
            self.speed *= -1
            self.move_couter *= -1

                # Cambiar la imagen del murciélago según la dirección
        if self.speed > 0:  # Si el murciélago se mueve hacia la derecha
            self.image = self.worm_left_images[self.worm_index // 5]
        else:  # Si el murciélago se mueve hacia la izquierda
            self.image = self.worm_left_images[self.worm_index // 5]

        self.worm_index += 1
        if self.worm_index >= len(self.worm_left_images) * 5:
            self.worm_index = 0

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
        self.player_hitbox = self.bat_hitbox.get_rect()  # Agregar esta línea

    def update(self):
        # Lógica de actualización del bat (movimiento por el eje x)
        self.rect.x += self.speed
        self.move_couter += 1
        if abs(self.move_couter) > 50:
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
        self.rect.y = y - 10
        self.speed = 6
        self.direction = direction
        # Crear la hitbox del proyectil (rectángulo rojo)
        self.hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.hitbox.fill(RED)
        self.miau_hitbox = self.hitbox.get_rect()

    def update(self):

        #mover el proyectil a derecha o izquierda
        self.rect.x += self.direction * self.speed
        # Eliminar el proyectil si sale de la pantalla
        if self.rect.y < 0 or self.rect.x < 0 or self.rect.x > WIDTH:
            self.kill()
        # Actualizar la posición de la hitbox del proyectil
        self.miau_hitbox.topleft = self.rect.topleft

        # Verificar colisiones con enemigos
        enemies_hit = pygame.sprite.spritecollide(self, bat_group, True)
        for enemy in enemies_hit:
            # Aquí puedes agregar lógica adicional si es necesario
            # por ejemplo, eliminar el proyectil y reducir la vida del enemigo
            bat_collision_sound.play()
            self.kill()
            player.score += 5
            star = Star(enemy.rect.x, enemy.rect.y)
            all_sprites.add(star)
            stars_group.add(star)

        worm_hit = pygame.sprite.spritecollide(self, worm_group, True)
        for worm in worm_hit:
            # Aquí puedes agregar lógica adicional si es necesario
            # por ejemplo, eliminar el proyectil y reducir la vida del enemigo
            bat_collision_sound.play()
            self.kill()
            player.score += 5
            star = Star(worm.rect.x, worm.rect.y - 25)
            all_sprites.add(star)
            stars_group.add(star)

def empty_groups():
    platform_group.empty()
    spell_book_group.empty()
    water_group.empty()
    lava_floor_group.empty()
    worm_group.empty()
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
player = Player(x=200, y= 350)
platform_group = pygame.sprite.Group()
spell_book_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
lava_floor_group = pygame.sprite.Group()
pumpkin_group = pygame.sprite.Group()
worm_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
lava_fire_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
bat_group = pygame.sprite.Group()
world = World(world_data)
stars_group = pygame.sprite.Group()
start_button = Button(WIDTH / 2 - 50, HEIGHT / 2 + 100, start_button_image)

# Crear grupo de sprites y agregar el jugador al grupo
miaus = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Bucle principal del juego
running = True
while running:

    game_over = player.update(game_over)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not player.can_shoot:
                player.shoot(player.direction)
                player.can_shoot = True
            else:
                player.can_shoot = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.direction = -1  # Si se suelta K_a, la direccion continua a la izquierda
            elif event.key == pygame.K_d:
                player.direction = 1

    # Actualizar
    platform_group.update()
    spell_book_group.update()
    water_group.update()
    lava_floor_group.update()
    worm_group.update()
    pumpkin_group.update()
    exit_group.update()
    fire_group.update()
    lava_fire_group.update()
    key_group.update()
    bat_group.update()
    all_sprites.update()
    stars_group.update()

    # Dibujar en la pantalla
    screen.fill(BLACK)

    world.draw()
    platform_group.draw(screen)
    spell_book_group.draw(screen)
    water_group.draw(screen)
    lava_floor_group.draw(screen)
    worm_group.draw(screen)
    pumpkin_group.draw(screen)
    exit_group.draw(screen)
    fire_group.draw(screen)
    lava_fire_group.draw(screen)
    key_group.draw(screen)
    bat_group.draw(screen)
    stars_group.draw(screen)
    all_sprites.draw(screen)

                # Dibujar información en la pantalla (Score, Lives, Keys)
    font = pygame.font.Font(None, 36)  # Puedes ajustar el tamaño de la fuente según tus preferencias

    spell_book_score = font.render("Spell Book: {0}".format(player.spell_book), True, GOLD)
    screen.blit(spell_book_score, (10, 130))

    # Renderizar texto para Score
    score_text = font.render("Score: {0}".format(player.score), True, GOLD)
    screen.blit(score_text, (10, 10))

    # Renderizar texto para Lives
    lives_text = font.render("Lives: {0}".format(player.lives), True, GOLD)
    screen.blit(lives_text, (10, 50))

    # Renderizar texto para Keys
    keys_text = font.render("Keys: {0}".format(player.key_score), True, GOLD)
    screen.blit(keys_text, (10, 90))

    if player.lives == 0:
        game_over_text = game_over_font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH / 2.5, HEIGHT / 2))

    if player.lives <= 0:
        # Mueve al jugador hacia abajo hasta que colisione con un tile
        player.image = rip_cat
        player.rect.y += 2
        for tile in world.tile_list:
            if tile[1].colliderect(player.rect.x, player.rect.y, player.width, player.height):
                # El jugador ha colisionado con un tile, detén el movimiento hacia abajo
                player.rect.y = tile[1].top - player.height
                break
            
        if start_button.draw(screen):
            pygame.mixer.music.play(-1)
            empty_groups()
            world.restart(world_data)
            player.restart(x=200, y= 250)
            game_over = 0

    if game_over == 1: 
        level += 1
        if level <= max_level:
            world_data = [[-1] * COLS for _ in range(ROWS)]
            with open("level{0}_data.csv".format(level), newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            # world.restart(world_data)
            player.restart(x=200, y= 250)
            game_over = 0
        else:
            pass
            

    # #Dibujar hitbox
    # for miau in miaus:
    #     pygame.draw.rect(screen, RED, miau.rect, 2)

    # for fire in fire_group:
    #     pygame.draw.rect(screen, WHITE, fire.rect, 2)

    # for lava in lava_group:
    #     pygame.draw.rect(screen, GRAY, lava.rect, 2)

    # for bat in bat_group:
    #     pygame.draw.rect(screen, ORANGE, bat.rect, 2)

    # #Dibujar hitbox del jugador
    # pygame.draw.rect(screen, GREEN, player.rect, 2)

    screen.blit(player.image, player.rect)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    pygame.time.Clock().tick(FPS)

# Salir del juego
pygame.quit()
sys.exit()




