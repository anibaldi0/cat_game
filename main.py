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


miau_cat = pygame.mixer.Sound(PATH_MIOU_CAT)
miau_cat.set_volume(0.2)

miau_right_image = pygame.transform.scale(pygame.image.load(MIAU_SOUND_IMAGE).convert_alpha(), (WIDTH / 16, HEIGHT / 16))
miau_left_image = pygame.transform.flip(miau_right_image, True, False)

walk_right_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH // 20, HEIGHT // 16)) for image in PLAYER_WALK_RIGHT_IMAGES_LIST]
walk_left_images = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(image).convert_alpha(),
                        (WIDTH // 20, HEIGHT // 16)), True, False) for image in PLAYER_WALK_RIGHT_IMAGES_LIST]

wall_image = pygame.transform.scale(pygame.image.load(WALL).convert_alpha(), (WIDTH / 16, HEIGHT / 20))
tree_image = pygame.transform.scale(pygame.image.load(TREE).convert_alpha(), (WIDTH / 16, HEIGHT / 11))

bat_left_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 17, HEIGHT / 17)) for image in BAT_LEFT_IMAGES_LIST]
bat_right_images = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(image).convert_alpha(), 
                        (WIDTH // 17, HEIGHT // 17)), True, False) for image in BAT_LEFT_IMAGES_LIST]

key_image = pygame.transform.scale(pygame.image.load(KEY).convert_alpha(), (WIDTH / 18, HEIGHT / 18))

star_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH / 24, HEIGHT / 20)) for image in STARS_LIST]


def draw_grid():
    for line in range(0, 10):
        pygame.draw.line(screen, WHITE, (0, line * tile_size), (WIDTH, line * tile_size))
        pygame.draw.line(screen, WHITE, (line * tile_size, 0), (line * tile_size, HEIGHT))

# Definir la clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
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
        self.jump_height = 15
        self.is_jumping = False
        self.jump_count = 10  # Inicializar jump_count aquí
        self.direction = 1
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.hitbox.fill(GREEN)
        self.hitbox_rect = self.hitbox.get_rect()  # Agregar esta línea
        self.player_hitbox = self.hitbox.get_rect()  # Agregar esta línea
        # Nueva variable para rastrear la cantidad de saltos realizados
        self.jump_count = 0
        self.max_jump_count = 2  # Establece el límite de saltos consecutivos
        self.score = 0

    def update(self):
        dx = 0
        dy = 0
        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        # Animación de caminar hacia la derecha
        if keys[pygame.K_d]:
            self.direction = 1
            self.rect.x += self.speed
            self.image = self.walk_images_right[self.walk_index // 5]  # Ajusta el divisor según la velocidad deseada de la animación
            self.walk_index += 1
            if self.walk_index >= len(self.walk_images_right) * 5:
                self.walk_index = 0

        # Animación de caminar hacia la izquierda
        if keys[pygame.K_a]:
            self.direction = -1
            self.rect.x -= self.speed
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
            # Incrementar la puntuación cuando el jugador colisiona con una estrella
            self.score += 1
            print("Puntuación:", self.score)

        #coordenadas de player
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            dy = 0
            
        screen.blit(self.image, self.rect)

    def shoot(self, direction):
        if direction == 1:
            miau = Miau(self.rect.right, self.rect.centery - 25, self.direction)
        else:
            miau = Miau(self.rect.left - 50, self.rect.centery - 25, self.direction)
        all_sprites.add(miau)
        miaus.add(miau)
        screen.blit(self.hitbox, self.player_hitbox)

    # def jump(self):
    #     if self.jump_count >= -10:
    #         neg = 1
    #         if self.jump_count < 0:
    #             neg = -1
    #         self.rect.y -= (self.jump_count ** 2) * 0.3 * neg
    #         self.jump_count -= 1
    #     else:
    #         self.is_jumping = False
    #         self.jump_count = 10

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
                if tile == 19:
                    key = key_image
                    key_rect = key.get_rect()
                    key_rect.x = col_count * tile_size
                    key_rect.y = row_count * tile_size + 15
                    tile = (key, key_rect)
                    self.tile_list.append(tile)
                if tile == 16:
                    bat = Enemy((col_count + 3) * tile_size, row_count * tile_size, random.choice([-1, 1]) * BAT_SPEED)
                    bat_group.add(bat)
                    
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, RED, tile[1], 2)

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
        self.hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.hitbox.fill(RED)
        self.star_hitbox = self.hitbox.get_rect()

    def update(self):
        # Actualizar la posición de la hitbox de la estrella
        self.star_hitbox.topleft = self.rect.topleft

        # Cambiar la imagen de la estrella según el índice
        self.image = self.star_images[self.star_index // 15]

        # Incrementar el índice para cambiar la imagen en el próximo ciclo
        self.star_index += 1
        if self.star_index >= len(self.star_images) * 15:
            self.star_index = 0

        # Renderizar la hitbox de la estrella
        screen.blit(self.hitbox, self.star_hitbox)

class Enemy(pygame.sprite.Sprite):
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
        self.hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.hitbox.fill(GREEN)
        self.hitbox_rect = self.hitbox.get_rect()  # Agregar esta línea
        self.player_hitbox = self.hitbox.get_rect()  # Agregar esta línea

    def update(self):
        # Lógica de actualización del enemigo (si es necesario)
        self.rect.x += self.speed
        self.move_couter += 1
        if abs(self.move_couter) > 90:
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
            self.kill()
            star = Star(enemy.rect.x, enemy.rect.y)
            all_sprites.add(star)
            stars_group.add(star)

        # Renderizar la hitbox del proyectil
        screen.blit(self.hitbox, self.miau_hitbox)

# Crear jugador
player = Player(x=200, y= 350)
bat_group = pygame.sprite.Group()
world = World(world_data)
stars_group = pygame.sprite.Group()

# Crear grupo de sprites y agregar el jugador al grupo
miaus = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Bucle principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.shoot(player.direction)
                miau_cat.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.direction = -1  # Si se suelta K_a, la direccion continua a la izquierda
            elif event.key == pygame.K_d:
                player.direction = 1

    # Verificar colisiones con enemigos
    enemies_hit = pygame.sprite.spritecollide(player, bat_group, True)
    for enemy in enemies_hit:
        # Aquí puedes agregar lógica adicional si es necesario
        # por ejemplo, reducir la vida del jugador al colisionar con un enemigo
        pass



    # Verificar colisiones con estrellas
    stars_hit = pygame.sprite.spritecollide(player, stars_group, True)
    for star in stars_hit:
        # Aquí puedes agregar lógica adicional si es necesario
        # por ejemplo, incrementar la puntuación del jugador al colisionar con una estrella
        pass

    # Actualizar
    all_sprites.update()
    bat_group.update()
    stars_group.update()

    # Dibujar en la pantalla
    screen.fill(BLACK)

    

    #Dibujar hitbox del proyectil
    # for miau in miaus:
        # pygame.draw.rect(screen, RED, miau.rect, 2)

    # # Dibujar hitbox de las plataformas
    # for platform in platforms:
    #     pygame.draw.rect(screen, GREEN, platform.hitbox_rect, 2)

    # draw_grid()

    # Dibujar hitbox del jugador
    # pygame.draw.rect(screen, GREEN, player.rect, 2)
    world.draw()
    bat_group.draw(screen)
    stars_group.draw(screen)
    all_sprites.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    pygame.time.Clock().tick(FPS)

# Salir del juego
pygame.quit()
sys.exit()




