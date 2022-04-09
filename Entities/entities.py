
import pygame

from math import copysign, sqrt

from Settings.settings import *
from Entities.spritesheet import *


def sign(x):
    '''
    Returns 1 if x is positive or null, -1 if x is negative.

    :param x: int to take sign from
    '''
    return copysign(1, x)


class Enemy(pygame.sprite.Sprite):
    """
    Allows to define what an enemy is within a game instance.
    It is caracterized by a spawning position pos (round tupple), hitporounds (hp) and a speed (vitesse).
    The move_enemy method allows to move it towards the player.

    :param game: a game instance in which the enemy is supposed to appear
    :param pos: the enemy's initial position
    :hp_max: the enemy's max hp (and initial hp)
    :atk: amount of damage dealt on attack
    :vitesse: speed
    :kb_res: resistance to knockback
    :loot: amount of gold dropped on death
    """

    def __init__(
        self,
        game,
        pos,
        hp_max=ENEMY_STAT[1]["HP_ENEMY_BASE"],
        atk=ENEMY_STAT[1]["ATK_ENEMY_BASE"],
        vitesse=ENEMY_STAT[1]["VIT_ENEMY_BASE"],
        kb_res=ENEMY_STAT[1]["KB_RES_BASE"],
        loot=ENEMY_STAT[1]["LOOT_BASE"]
    ):
        self.game = game

        # Enemy settings
        self.player_pos = self.game.player.pos #player position
        self.pos = pos #enemy position
        self.hp_max = hp_max
        self.hp = self.hp_max
        self.atk = atk
        self.vitesse = vitesse
        self.kb_res = kb_res # knockback resistance
        self.loot = loot # amount of gold to drop on death
        self.last_update = 0
        self.animation_cooldown = 10 ** 89

        # Creating the object that will be drawn
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def move_enemy(self):
        """
        Moves the enemy towards the player.
        Enemies that are to close to the player along any axis will not move along that axis.
        """

        xp = self.player_pos[0]
        yp = self.player_pos[1]

        (xe, ye) = self.pos

        sx = sign(xp - xe)
        sy = sign(yp - ye)

        if abs(xe - xp) > mvt_acccy:
            if abs(ye - yp) > mvt_acccy:
                # Movement is slowed down in each direction for diagonals,
                # so that the overall norm stays almost the same
                self.pos[0] += sx * round(self.vitesse * sqrt(0.5))
                self.rect.x += sx * round(self.vitesse * sqrt(0.5))
                self.pos[1] += sy * round(self.vitesse * sqrt(0.5))
                self.rect.y += sy * round(self.vitesse * sqrt(0.5))
            else:
                self.pos[0] += sx * round(self.vitesse)
                self.rect.x += sx * round(self.vitesse)
        elif abs(ye - yp) > mvt_acccy:
            self.pos[1] += sy * round(self.vitesse)
            self.rect.y += sy * round(self.vitesse)

    def knockbacks_enemy_player(self, kb_amount):
        """
        Knocks the enemy back by kb_amount
        :param kb_amount: amount of applied knockback
        """
        x = self.player_pos[0]
        y = self.player_pos[1]

        if x < self.pos[0]:
            self.pos[0] += max(0, round(kb_amount - self.kb_res))
            self.rect.x += max(0, round(kb_amount - self.kb_res))

        elif x > self.pos[0]:
            self.pos[0] -= max(0, round(kb_amount - self.kb_res))
            self.rect.x -= max(0, round(kb_amount - self.kb_res))

        if y < self.pos[1]:
            self.pos[1] += max(0, kb_amount - self.kb_res)
            self.rect.y += max(0, kb_amount - self.kb_res)

        elif y > self.pos[1]:
            self.pos[1] -= max(0, kb_amount - self.kb_res)
            self.rect.y -= max(0, kb_amount - self.kb_res)

    def knockbacks_enemy_wall(self, dirx, diry):
        """
        Pushes the enemy away from a wall, pixel by pixel.
        :param dirx: direction of pushing along the x axis, with -1 for going left, 1 for right, 0 for none
        :param diry: direction of pushing along the y axis, with -1 for going up, 1 for down, 0 for none
        """
        self.pos[0] += dirx
        self.rect.x += dirx
        self.pos[1] += diry
        self.rect.y += diry

    def hurt(self, dmg):
        """
        Lowers the enemy hp by dmg.

        :param dmg: int to substract from the player's hp
        """
        self.hp -= dmg

    def update_enemy(self):
        """
        Updates the enemy's position, as well as its lifebars's.
        """
        self.player_pos = self.game.player.pos
        self.move_enemy()
        self.game.enemy_lifebars_outline[self].move()
        self.game.enemy_lifebars[self].move()


class BaseEnemy(Enemy):
    '''
    Represents a regular enemy.

    :param game: a game instance in which the enemy is supposed to appear
    :param pos: the enemy's initial position
    :param difficulty: the chosen difficulty, changes the enemy's stats
    '''
    def __init__(self, game, pos, difficulty):
        Enemy.__init__(
            self,
            game,
            pos,
            ENEMY_STAT[difficulty]["HP_ENEMY_BASE"],
            ENEMY_STAT[difficulty]["ATK_ENEMY_BASE"],
            ENEMY_STAT[difficulty]["VIT_ENEMY_BASE"],
            ENEMY_STAT[difficulty]["KB_RES_BASE"],
            ENEMY_STAT[difficulty]["LOOT_BASE"]
        )
        self.animation_steps = 4
        self.last_update = -1
        self.animation_cooldown = 75
        self.frame = 0

        self.sprite_sheet = pygame.image.load("Sprites/enemy_utile.png").convert_alpha()
        self.animation_list = []

        # Adding frames into the list
        image1 = pygame.Surface((16, 16)).convert_alpha()
        image1.blit(self.sprite_sheet, (-1, 0))
        image1 = pygame.transform.scale(image1, (16 * 2, 16 * 2))
        image1.set_colorkey(WHITE)
        self.animation_list.append(image1)

        image2 = pygame.Surface((16, 16)).convert_alpha()
        image2.blit(self.sprite_sheet, (-19, 0))
        image2 = pygame.transform.scale(image2, (16 * 2, 16 * 2))
        image2.set_colorkey(WHITE)
        self.animation_list.append(image2)

        image3 = pygame.Surface((16, 16)).convert_alpha()
        image3.blit(self.sprite_sheet, (-37, 0))
        image3 = pygame.transform.scale(image3, (16 * 2, 16 * 2))
        image3.set_colorkey(WHITE)
        self.animation_list.append(image3)

        image4 = pygame.Surface((16, 16)).convert_alpha()
        image4.blit(self.sprite_sheet, (-55, 0))
        image4 = pygame.transform.scale(image4, (16 * 2, 16 * 2))
        image4.set_colorkey(WHITE)
        self.animation_list.append(image4)

        # Displaying sprites
        self.image = self.animation_list[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.game.all_sprites.add(self)


class RushEnemy(Enemy):
    '''
    Represents a Rush enemy (fast with low health, attack and loot).

    :param game: a game instance in which the enemy is supposed to appear
    :param pos: the enemy's initial position
    :param difficulty: the chosen difficulty, changes the enemy's stats
    '''
    def __init__(self, game, pos, difficulty):
        Enemy.__init__(
            self,
            game,
            pos,
            ENEMY_STAT[difficulty]["HP_ENEMY_LOW"],
            ENEMY_STAT[difficulty]["ATK_ENEMY_LOW"],
            ENEMY_STAT[difficulty]["VIT_ENEMY_HIGH"],
            ENEMY_STAT[difficulty]["KB_RES_LOW"],
            ENEMY_STAT[difficulty]["LOOT_LOW"]
        )
        self.animation_steps = 2
        self.last_update = -1
        self.animation_cooldown = 75
        self.frame = 0

        self.sprite_sheet = pygame.image.load("Sprites/enemy_utile.png").convert_alpha()
        self.animation_list = []

        # Adding frames into the list
        image1 = pygame.Surface((8, 10)).convert_alpha()
        image1.blit(self.sprite_sheet, (-77, -3))
        image1 = pygame.transform.scale(image1, (8 * 2, 10 * 2))
        image1.set_colorkey(WHITE)
        self.animation_list.append(image1)

        image2 = pygame.Surface((16, 8)).convert_alpha()
        image2.blit(self.sprite_sheet, (-90, -5))
        image2 = pygame.transform.scale(image2, (16 * 2, 8 * 2))
        image2.set_colorkey(WHITE)
        self.animation_list.append(image2)

        # Displaying sprites
        self.image = self.animation_list[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.game.all_sprites.add(self)


class TankEnemy(Enemy):
    '''
    Represents a Tank enemy (slow with high attack, speed and loot).

    :param game: a game instance in which the enemy is supposed to appear
    :param pos: the enemy's initial position
    :param difficulty: the chosen difficulty, changes the enemy's stats
    '''
    def __init__(self, game, pos, difficulty):
        Enemy.__init__(
            self,
            game,
            pos,
            ENEMY_STAT[difficulty]["HP_ENEMY_HIGH"],
            ENEMY_STAT[difficulty]["ATK_ENEMY_HIGH"],
            ENEMY_STAT[difficulty]["VIT_ENEMY_LOW"],
            ENEMY_STAT[difficulty]["KB_RES_HIGH"],
            ENEMY_STAT[difficulty]["LOOT_HIGH"]
        )
        self.animation_steps = 2
        self.last_update = -1
        self.animation_cooldown = 75
        self.frame = 0

        self.sprite_sheet = pygame.image.load("Sprites/enemy_utile.png").convert_alpha()

        self.animation_list = []

        # Adding frames into the list up
        image1 = pygame.Surface((14, 16)).convert_alpha()
        image1.blit(self.sprite_sheet, (-107, 0))
        image1 = pygame.transform.scale(image1, (14 * 2, 16 * 2))
        image1.set_colorkey(WHITE)
        self.animation_list.append(image1)

        image2 = pygame.Surface((16, 15)).convert_alpha()
        image2.blit(self.sprite_sheet, (-123, -1))
        image2 = pygame.transform.scale(image2, (16 * 2, 15 * 2))
        image2.set_colorkey(WHITE)
        self.animation_list.append(image2)

        # Displaying sprites
        self.image = self.animation_list[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.game.all_sprites.add(self)


class BossEnemy(Enemy):
    '''
    Represents a Boss enemy.

    :param game: a game instance in which the enemy is supposed to appear
    :param pos: the enemy's initial position
    :param difficulty: the chosen difficulty, changes the enemy's stats
    '''
    def __init__(self, game, pos, difficulty):
        Enemy.__init__(
            self,
            game,
            pos,
            ENEMY_STAT[difficulty]["HP_ENEMY_BOSS"],
            ENEMY_STAT[difficulty]["ATK_ENEMY_HIGH"],
            ENEMY_STAT[difficulty]["VIT_ENEMY_BASE"],
            ENEMY_STAT[difficulty]["KB_RES_HIGH"],
            ENEMY_STAT[difficulty]["LOOT_SUPER"]
        )
        self.animation_steps = 4
        self.last_update = -1
        self.animation_cooldown = 75
        self.frame = 0

        self.sprite_sheet_image_1 = pygame.image.load(
            "Sprites/champi_m1.png"
        ).convert_alpha()
        self.sprite_sheet_image_2 = pygame.image.load(
            "Sprites/champi_m2.png"
        ).convert_alpha()
        self.sprite_sheet_image_3 = pygame.image.load(
            "Sprites/champi_m3.png"
        ).convert_alpha()
        self.sprite_sheet_image_4 = pygame.image.load(
            "Sprites/champi_m4.png"
        ).convert_alpha()

        self.sprite_sheet_1 = SpriteSheet(self.sprite_sheet_image_1)
        self.sprite_sheet_2 = SpriteSheet(self.sprite_sheet_image_2)
        self.sprite_sheet_3 = SpriteSheet(self.sprite_sheet_image_3)
        self.sprite_sheet_4 = SpriteSheet(self.sprite_sheet_image_4)

        self.animation_list = []

        # Adding frames into the list
        self.animation_list.append(
            self.sprite_sheet_1.get_image((0, 0), 0, 71, 71, 1, WHITE)
        )
        self.animation_list.append(
            self.sprite_sheet_2.get_image((0, 0), 0, 70, 71, 1, WHITE)
        )
        self.animation_list.append(
            self.sprite_sheet_3.get_image((0, 0), 0, 65, 69, 1, WHITE)
        )
        self.animation_list.append(
            self.sprite_sheet_4.get_image((0, 0), 0, 69, 71, 1, WHITE)
        )

        # Displaying sprites
        self.image = self.animation_list[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.game.all_sprites.add(self)


class Wall(pygame.sprite.Sprite):
    '''
    Represents a wall, which blocks the other entities.

    :param game: the game instance of the wall
    :param direction:
    :param x1: x coordinate of the first corner
    :param x2: x coordinate of the second corner (opposite to the first one)
    :param y1: y coordinate of the first corner
    :param y2: y coordinate of the second corner (opposite to the first one)
    '''
    
    def __init__(self, game, direction, x1, x2, y1, y2):
        self.game = game
        self.direction = direction
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        # Knockback direction depending on the direction of the wall, so as to push
        # the player or the enemies away from it and towards the center of the map
        self.kb_dir = {"up": [0, 1], "down": [0, -1], "left": [1, 0], "right": [-1, 0]}

        # Displaying sprites
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([abs(x1 - x2), abs(y1 - y2)])
        self.rect = self.image.get_rect()
        self.rect.center = [(x1 + x2) // 2, (y1 + y2) // 2]

    def knockbacks_player(self):
        '''
        Pushes the player away from the wall, towards the center of the map.
        '''
        while pygame.sprite.spritecollideany(self.game.player, [self]):
            self.game.player.move(
                self.kb_dir[self.direction][0], self.kb_dir[self.direction][1]
            )

    def knockbacks_enemy(self, enemy):
        '''
        Pushes an enemy away from the wall, towards the center of the map.
        '''
        while pygame.sprite.spritecollideany(enemy, [self]):
            enemy.knockbacks_enemy_wall(
                self.kb_dir[self.direction][0], self.kb_dir[self.direction][1]
            )

