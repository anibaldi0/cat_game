import pygame
import sys
from constants import *
import random
from images import *
from sounds import *

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("     Natacha's game")
icon = pygame.image.load(ICON_PATH)
pygame.display.set_icon(icon)

miau_cat = pygame.mixer.Sound(PATH_MIOU_CAT)
miau_cat.set_volume(0.2)

miau_right_image = pygame.transform.scale(pygame.image.load(MIAU_SOUND_IMAGE).convert_alpha(), (WIDTH / 10, HEIGHT / 15))
miau_left_image = pygame.transform.flip(miau_right_image, True, False)

walk_right_images = [pygame.transform.scale(pygame.image.load(image).convert_alpha(), (WIDTH // 10, HEIGHT // 10)) for image in PLAYER_WALK_RIGHT_IMAGES]
walk_left_images = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(image).convert_alpha(),
                        (WIDTH // 10, HEIGHT // 10)), True, False) for image in PLAYER_WALK_RIGHT_IMAGES]

# Definir la clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Nuevas propiedades para la animación de caminar
        self.walk_index = 0
        self.walk_images_right = walk_right_images
        self.walk_images_left = walk_left_images

        self.image = self.walk_images_right[0] #el juego empieza con player a la derecha
        self.rect = self.image.get_rect()
        self.rect.center = (250, 475)
        self.speed = 3
        self.jump_height = 15
        self.is_jumping = False
        self.jump_count = 10  # Inicializar jump_count aquí
        self.direction = 1
        self.hitbox = pygame.Surface((self.rect.width, self.rect.height))
        self.hitbox.fill(GREEN)
        self.hitbox_rect = self.hitbox.get_rect()  # Agregar esta línea
        self.player_hitbox = self.hitbox.get_rect()  # Agregar esta línea

    def update(self):
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

        # Controlar el salto
        if keys[pygame.K_SPACE]:
            if not self.is_jumping:
                self.is_jumping = True

        # Aplicar la gravedad si el jugador está en el aire
        if self.is_jumping:
            self.jump()

        # # Restablecer la posición vertical al suelo si hay colisión con una plataforma
        # platform_hit = pygame.sprite.spritecollide(self, platforms, False)
        # if platform_hit:
        #     # Verificar si la colisión es en la parte superior de la plataforma
        #     if self.rect.colliderect(platform_hit[0].rect):
        #         self.rect.y = platform_hit[0].rect.y - self.rect.height
        #         self.is_jumping = False
        #         self.jump_count = 10

        # # Restablecer la posición vertical al suelo si está en el borde inferior de la pantalla
        # if self.rect.bottom >= HEIGHT:
        #     self.rect.bottom = HEIGHT
        #     self.is_jumping = False
        #     self.jump_count = 10

        # # Restablecer la posición horizontal si está en los bordes laterales de la pantalla
        # if self.rect.left <= 0:
        #     self.rect.left = 0
        # elif self.rect.right >= WIDTH:
        #     self.rect.right = WIDTH

        # # Actualizar la posición del hitbox
        # self.hitbox_rect.topleft = self.rect.topleft

    def shoot(self):
        if self.direction == 1:
            miau = Miau(self.rect.right, self.rect.centery - 25, self.direction)
        else:
            miau = Miau(self.rect.left - 50, self.rect.centery - 25, self.direction)
        all_sprites.add(miau)
        miaus.add(miau)
        screen.blit(self.hitbox, self.player_hitbox)

    def jump(self):
        if self.jump_count >= -10:
            neg = 1
            if self.jump_count < 0:
                neg = -1
            self.rect.y -= (self.jump_count ** 2) * 0.3 * neg
            self.jump_count -= 1
        else:
            self.is_jumping = False
            self.jump_count = 10
            self.rect.centery = 475  # Restablecer la posición vertical al suelo después del salto

# class Platform(pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height):
#         super().__init__()
#         self.image = pygame.Surface((width, height))
#         self.image.fill(BLUE)  # Puedes cambiar el color o cargar una imagen para la plataforma
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y

#         # Agregar hitbox
#         self.hitbox = pygame.Surface((width, height))
#         self.hitbox.fill(RED)
#         self.hitbox_rect = self.hitbox.get_rect()
#         self.hitbox_rect.topleft = self.rect.topleft

#     def update(self):
#         # Actualizar la posición de la hitbox con la posición de la plataforma
#         self.hitbox_rect.topleft = self.rect.topleft


class Enemy(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 500 - self.rect.width)  # Posición X aleatoria
        self.rect.y = random.randrange(0, 200)  # Posición Y aleatoria
        self.speed = random.randint(1, 5)  # Velocidad aleatoria

    def update(self):
        # Lógica de actualización del enemigo (si es necesario)
        self.rect.y += self.speed
        if self.rect.y > 500:
            # Restablecer la posición del enemigo si sale de la pantalla
            self.rect.y = random.randrange(-30, -10)
            self.rect.x = random.randrange(0, 500 - self.rect.width)
            self.speed = random.randint(1, 5)

# Definir la clase Miau (proyectil)
class Miau(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        if direction == 1:
            self.image = miau_right_image
        else:
            self.image = miau_left_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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

        # Renderizar la hitbox del proyectil
        screen.blit(self.hitbox, self.miau_hitbox)

# Crear jugador
player = Player()
enemy = Enemy()

# # Crear plataformas
# platform1 = Platform(50, 400, 200, 20)
# platform2 = Platform(300, 300, 200, 20)

# # Crear grupo de plataformas
# platforms = pygame.sprite.Group()
# platforms.add(platform1, platform2)

# Crear grupo de sprites y agregar el jugador al grupo
miaus = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy)

# Bucle principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.shoot()
                miau_cat.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.direction = -1  # Si se suelta K_a, la direccion continua a la izquierda
            elif event.key == pygame.K_d:
                player.direction = 1

    # Actualizar
    all_sprites.update()

    # Dibujar en la pantalla
    screen.fill(BLACK)

    # Dibujar hitbox del jugador
    pygame.draw.rect(screen, GREEN, player.rect, 2)
    #Dibujar hitbox del proyectil
    # for miau in miaus:
        # pygame.draw.rect(screen, RED, miau.rect, 2)

    # # Dibujar hitbox de las plataformas
    # for platform in platforms:
    #     pygame.draw.rect(screen, GREEN, platform.hitbox_rect, 2)

    all_sprites.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    pygame.time.Clock().tick(FPS)

# Salir del juego
pygame.quit()
sys.exit()




