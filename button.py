
import pygame

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
    

    