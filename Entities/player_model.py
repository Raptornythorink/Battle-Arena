import pygame

from Entities.spritesheet import *
from Settings.settings import *


class PlayerModel(pygame.sprite.Sprite):
    """
    Constructs the sprite of the Player, frame by frame.
    """
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.pos = self.player.pos

        self.animation_steps = 2
        self.last_update = -1
        self.animation_cooldown = 100
        self.frame = 0

        pygame.sprite.Sprite.__init__(self)

        # Creating the sprite_sheet, the frame is fetched inside the sheet thanks to the method .get_image defined in spritesheet.py

        self.sprite_sheet_image_left = pygame.image.load(
            "Sprites/link_sprites_left.png"
        ).convert_alpha()
        self.sprite_sheet_image_down = pygame.image.load(
            "Sprites/link_sprites_down.png"
        ).convert_alpha()
        self.sprite_sheet_image_up = pygame.image.load(
            "Sprites/link_sprites_up.png"
        ).convert_alpha()
        self.sprite_sheet_image_right = pygame.image.load(
            "Sprites/link_sprites_right.png"
        ).convert_alpha()

        self.sprite_sheet_left = SpriteSheet(self.sprite_sheet_image_left)
        self.sprite_sheet_down = SpriteSheet(self.sprite_sheet_image_down)
        self.sprite_sheet_up = SpriteSheet(self.sprite_sheet_image_up)
        self.sprite_sheet_right = SpriteSheet(self.sprite_sheet_image_right)

        self.animation_list_left = []
        self.animation_list_right = []
        self.animation_list_up = []
        self.animation_list_down = []

        # Add left direction sprites
        self.animation_list_left.append(
            self.sprite_sheet_left.get_image((0, 0), 0, 16, 16, 2, SPRITE_BACKGROUND)
        )
        self.animation_list_left.append(
            self.sprite_sheet_left.get_image((0, 0), 1, 16, 16, 2, SPRITE_BACKGROUND)
        )

        # Add right direction sprites
        self.animation_list_right.append(
            self.sprite_sheet_right.get_image((0, 0), 0, 14, 16, 2, SPRITE_BACKGROUND)
        )
        self.animation_list_right.append(
            self.sprite_sheet_right.get_image((0, 0), 1, 14, 16, 2, SPRITE_BACKGROUND)
        )

        # Add up direction
        self.animation_list_up.append(
            self.sprite_sheet_up.get_image((0, 0), 0, 14, 16, 2, SPRITE_BACKGROUND)
        )
        self.animation_list_up.append(
            self.sprite_sheet_up.get_image((0, 0), 1, 14, 16, 2, SPRITE_BACKGROUND)
        )
        # Add down direction
        self.animation_list_down.append(
            self.sprite_sheet_down.get_image((0, 0), 0, 15, 16, 2, SPRITE_BACKGROUND)
        )
        self.animation_list_down.append(
            self.sprite_sheet_down.get_image((0, 0), 1, 15, 16, 2, SPRITE_BACKGROUND)
        )

        #Displaying sprites
        self.image = self.animation_list_right[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.game.all_sprites.add(self)

    def update_pos(self):
        '''
        Updates the model's position so as to follow the player's hurtbox.
        '''
        self.rect.center = self.player.rect.center
