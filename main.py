import pygame
import sys

# from pygame.sprite import _Group
from constants import *
import random
from images import *
from sounds import *
from maps import *

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

lava_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 16, HEIGHT / 22)) for image in LAVA_IMAGES_LIST]

fire_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 20, HEIGHT / 10)) for image in FIRE_IMAGES_LIST]

key_image = pygame.transform.scale(pygame.image.load(KEY).convert_alpha(), (WIDTH / 18, HEIGHT / 18))

star_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 24, HEIGHT / 20)) for image in STARS_LIST]

door_image = pygame.transform.scale(pygame.image.load(DOOR_IMAGE).convert_alpha(), (WIDTH / 16, HEIGHT / 16))

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
            


            # Verificar colisiones con estrellas
            stars_hit = pygame.sprite.spritecollide(self, stars_group, True)
            for star in stars_hit:
                star_coin_sound.play()
                self.score += 1
                print("Puntuación:", self.score)

            # Verificar colisiones con enemigos
            bat_hit = pygame.sprite.spritecollide(player, bat_group, False)
            for bat in bat_hit:
                if player.rect.colliderect(bat.rect):
                    player_death_sound.play()
                    player.lives -= 1
                    game_over = -1
                    print(player.lives)
            if player.rect.y < 0:
                player.rect.x = 200
                player.rect.y = 255
                    

            key_hit = pygame.sprite.spritecollide(self, key_group, True)
            for key in key_hit:
                key_sound.play()
                self.key_score += 1
                print("Llaves: {0}".format(self.key_score))

            fire_hit = pygame.sprite.spritecollide(self, fire_group, False)
            for fire in fire_hit:
                player_death_sound.play()
                player.lives -= 1
                game_over = -1
                player.image = cat_death_image
                

            lava_hit = pygame.sprite.spritecollide(self, lava_group, False)
            for lava in lava_hit:
                player_death_sound.play(1)
                player.lives -= 1
                game_over = -1
                player.image = cat_death_image
                self.rect.y -= 2
                

            door_hit = pygame.sprite.spritecollide(self, door_group, False)
            for door in door_hit:
                if self.key_score > 0:
                    door_open_sound.play(1)
                else:
                    player_death_sound.play()
                    player.lives -= 1
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
            # print(game_over)
            self.image = cat_death_image
            self.rect.y -= 5
            if self.rect.y < -80:
                game_over = 0
            if self.lives == 0:
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
                if tile == 5:
                    door = Door(col_count * tile_size, row_count * tile_size + 15)
                    door_group.add(door)
                if tile == 19:
                    key = Key(col_count * tile_size, row_count * tile_size + 15)
                    key_group.add(key)
                if tile == 16:
                    bat = Bat(col_count * tile_size, row_count * tile_size, random.choice([-1, 1]) * BAT_SPEED)
                    bat_group.add(bat)
                if tile == 2:
                    lava = Lava(col_count * tile_size, row_count * tile_size)
                    lava_group.add(lava)
                if tile == 6:
                    fire = Fire(col_count * tile_size, row_count + 9.45 * tile_size, FIRE_SPEED)
                    fire_group.add(fire)
                    
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, RED, tile[1], 2)

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

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = door_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  # Ajustar la posición vertical según sea necesario
        self.door_hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.door_hitbox.fill(RED)
        self.door_hitbox_rect = self.door_hitbox.get_rect()

    def update(self):
        # Actualizar la posición de la hitbox de la llave
        self.door_hitbox_rect.topleft = self.rect.topleft
        # Renderizar la hitbox de la llave
        screen.blit(self.door_hitbox, self.door_hitbox_rect)

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.lava_index = 0
        self.lava_images = lava_images
        self.image = lava_images[0]
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
        self.image = self.lava_images[self.lava_index // 10]

        # Incrementar el índice para cambiar la imagen en el próximo ciclo
        self.lava_index += 1
        if self.lava_index >= len(self.lava_images) * 10:
            self.lava_index = 0

        # Renderizar la hitbox de la estrella
        # screen.blit(self.lava_hitbox, self.lava_hitbox)

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
        # self.rect.y += self.speed
        # self.move_couter += 1
        # if abs(self.move_couter) > 12:
        #     self.speed *= -1
        #     self.move_couter *= -1

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
            star = Star(enemy.rect.x, enemy.rect.y)
            all_sprites.add(star)
            stars_group.add(star)

# Crear jugador
player = Player(x=200, y= 350)
door_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
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
    door_group.update()
    fire_group.update()
    lava_group.update()
    key_group.update()
    bat_group.update()
    all_sprites.update()
    stars_group.update()

    # Dibujar en la pantalla
    screen.fill(BLACK)

            # Dibujar información en la pantalla (Score, Lives, Keys)
    font = pygame.font.Font(None, 36)  # Puedes ajustar el tamaño de la fuente según tus preferencias

    # Renderizar texto para Score
    score_text = font.render("Score: {0}".format(player.score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Renderizar texto para Lives
    lives_text = font.render("Lives: {0}".format(player.lives), True, WHITE)
    screen.blit(lives_text, (10, 50))

    # Renderizar texto para Keys
    keys_text = font.render("Keys: {0}".format(player.key_score), True, WHITE)
    screen.blit(keys_text, (10, 90))

    if player.lives == 0:
        game_over_text = game_over_font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH / 2.5, HEIGHT / 2))

    world.draw()
    door_group.draw(screen)
    fire_group.draw(screen)
    lava_group.draw(screen)
    key_group.draw(screen)
    bat_group.draw(screen)
    stars_group.draw(screen)
    all_sprites.draw(screen)

    if player.lives == 0:
        # Mueve al jugador hacia abajo hasta que colisione con un tile
        player.rect.y += 2
        for tile in world.tile_list:
            if tile[1].colliderect(player.rect.x, player.rect.y, player.width, player.height):
                # El jugador ha colisionado con un tile, detén el movimiento hacia abajo
                player.rect.y = tile[1].top - player.height
                break
        player.image = rip_cat
        if start_button.draw(screen):
            player.restart(x=200, y= 250)
            game_over = 0

    #Dibujar hitbox
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

    # pygame.draw.rect(screen, GREEN, door.rect, 2)

    screen.blit(player.image, player.rect)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    pygame.time.Clock().tick(FPS)

# Salir del juego
pygame.quit()
sys.exit()




