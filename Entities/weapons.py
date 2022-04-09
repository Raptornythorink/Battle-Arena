import pygame
from Settings.settings import *


class Weapon(pygame.sprite.Sprite):
    """
    Represents a weapon used to play and its characteristics.

    :param game: the game instance of the weapon
    :param atk: the weapon's attack value
    :param range: the weapon's range
    :param kb: the weapon's knockback inflicted on enemies on hit
    :param cooldown: the minimum time between two strikes
    :param width: width used to position the weapon on the player
    :param height: height used to position the weapon on the player
    """
    def __init__(self, game, atk=ATK_DMG, range = ATK_RANGE, kb = KB_WP, cooldown = ATK_CD, width=10, height=10):
        self.game = game
        self.player = self.game.player
        self.atk = atk
        self.range = range
        self.kb = kb
        self.cooldown = cooldown
        self.width = width
        self.height = height

        self.animation = False

        # Settings
        self.weapon_dir_x = {"up": 0, "down": 0, "left": (self.width - TILESIZE) // 2,"right": (TILESIZE  - self.width)// 2}
        self.weapon_dir_y = {"up": (self.height - TILESIZE) // 2, "down": (TILESIZE - self.height) // 2, "left": 0,"right": 0}

        self.weapon_anim_dir_x = {"up": 0, "down": 0, "left": (- self.width - TILESIZE) // 2,"right": (TILESIZE  + self.width)// 2}
        self.weapon_anim_dir_y = {"up": (- self.height - TILESIZE) // 2, "down": (TILESIZE + self.height) // 2, "left": 0,"right": 0}

        self.pos = [self.player.pos[0] + self.weapon_dir_x[self.player.facing],
                    self.player.pos[1] + self.weapon_dir_y[self.player.facing]]

        # Creating the object that will be drawn
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet_image = pygame.image.load("Sprites/link.png")
        width_sword = 7
        height_sword = 15
        self.image = pygame.Surface([width_sword, height_sword]).convert_alpha()
        self.image.fill(YELLOW)
        corner = (-52, -137)
        self.image.blit(self.sprite_sheet_image, corner)
        self.image = pygame.transform.scale(self.image, (width_sword * 1.5, height_sword * 1.5))
        self.image.set_colorkey(SPRITE_BACKGROUND)
        self.image_copy = self.image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.game.all_sprites.add(self)
        self.playing_wall_tap = False
    
    
    def update_weapon(self):
        '''
        Updates the weapon's position according the the player's position and orientation.
        '''
        if self.animation and pygame.time.get_ticks() - self.game.player.last_attack_date > self.cooldown:
            self.animation = False
            self.playing_wall_tap = False

        if self.animation:
            self.directions_x = self.weapon_anim_dir_x
            self.directions_y = self.weapon_anim_dir_y
        else:
            self.directions_x = self.weapon_dir_x
            self.directions_y = self.weapon_dir_y

        self.pos[0] = self.player.pos[0] + self.directions_x[self.player.facing]
        self.pos[1] = self.player.pos[1] + self.directions_y[self.player.facing]
        self.rect.center = self.pos

        if self.player.facing == "up":
            self.image = self.image_copy
        if self.player.facing == "down":
            self.image = pygame.transform.rotate(self.image_copy, 180)
        if self.player.facing == "left":
            self.image = pygame.transform.rotate(self.image_copy, 90)
        if self.player.facing == "right":
            self.image = pygame.transform.rotate(self.image_copy, -90)
        self.image.set_colorkey(SPRITE_BACKGROUND)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.game.all_sprites.add(self)






