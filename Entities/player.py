import pygame

from Settings.settings import *

from Entities.lifebar import *
from Entities.spritesheet import *


class Player(pygame.sprite.Sprite):
    '''
    Represents a player and its characteristics.
    '''
    def __init__(self, game, pos):
        self.game = game
        self.myfont = pygame.font.SysFont(FONT, 50)

        # Settings
        self.pos = pos
        self.vitesse = VIT_PL
        self.hp_max = HP_PL_BASE
        self.hp = self.hp_max
        self.kb = KB_PL_BASE # knockback inflicted to enemies when hurt
        self.gold = 0
        self.facing = "up"
        self.last_attack_date = -1
        self.score = 0

        # Creating the object that will be drawn
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([TILESIZE, TILESIZE])
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def move(self, dirx, diry):
        """
        Moves the player's rectangle along the x and y axis.

        :param dirx: direction, -1 for left, 1 for right, 0 for none
        :param diry: direction, -1 for down, 1 for up, 0 for none
        """
        if dirx == 0 or diry == 0:
            self.rect.x += round(self.vitesse * dirx)
            self.rect.y += round(self.vitesse * diry)
            self.pos[0] += round(self.vitesse * dirx)
            self.pos[1] += round(self.vitesse * diry)
        else:
            # mouvement is slowed down along each axis in diagonals,
            # so that the overall norm stays almost the same
            self.rect.x += round(self.vitesse * dirx * sqrt(0.5))
            self.rect.y += round(self.vitesse * diry * sqrt(0.5))
            self.pos[0] += round(self.vitesse * dirx * sqrt(0.5))
            self.pos[1] += round(self.vitesse * diry * sqrt(0.5))
        self.rect.center = self.pos

    def hurt(self, dmg):
        """
        Lowers the player's hp by dmg, and plays a sound.
        If the player's hp reaches 0, initiates the game loss process.

        :param dmg: int to substract from the player's hp
        """
        self.hp -= dmg
        self.game.sound_effects
        self.game.lifebar_player.update_lifebar()
        if self.hp <= 0:
            self.game.lost()
        pygame.mixer.Sound.play(self.game.sound_effects.player_hurt)


    def heal(self, heal):
        """
        Increases the player's hp by heal or sets it to self.hp_max if heal is too high.

        :param heal: int to add to the player's hp
        """
        self.hp = min(self.hp + heal, self.hp_max)
        self.game.lifebar_player.update_lifebar()

    def in_attack_range(self, enemy):
        """
        Returns a boolean indicating whether an enemy is in attack range of the player,
        taking its direction into account.

        :param enemy: 
        """
        (x_pl, y_pl) = self.rect.center
        (x_en, y_en) = enemy.pos

        if self.facing == "up":
            return (
                abs(x_en - x_pl) < ATK_RANGE
                and -y_pl < -y_en
                and -y_pl + ATK_RANGE > -y_en
            )

        elif self.facing == "down":
            return (
                abs(x_en - x_pl) < ATK_RANGE
                and -y_pl > -y_en
                and -y_pl - ATK_RANGE < -y_en
            )

        elif self.facing == "right":
            return (
                abs(y_en - y_pl) < ATK_RANGE and x_pl < x_en and x_pl +
                ATK_RANGE > x_en
            )

        else:
            return (
                abs(y_en - y_pl) < ATK_RANGE and x_pl > x_en and x_pl -
                ATK_RANGE < x_en
            )

    def attack(self):
        """
        Makes the player attack in the direction he faces (in ["up", "down", "left", "right"]).
        """
        if not self.game.weapon.animation:
            self.last_attack_date = pygame.time.get_ticks()
            self.game.weapon.animation = True
            self.game.sound_effects.play_sword_slash()
            for enemy in self.game.enemies:
                if self.in_attack_range(enemy):
                    enemy.hurt(self.game.weapon.atk)
                    enemy.knockbacks_enemy_player(self.game.weapon.kb)
                    self.game.enemy_lifebars[enemy].update_lifebar()

    def update_pl_facing(self, direction):
        """
        Updates the direction the player faces

        :param dir: in ["up, "down", "left", "right"]
        """
        self.facing = direction

    def add_gold(self, loot):
        '''
        Increases the player's gold.

        :param loot: amount of gold to add
        '''
        self.gold += loot

    def add_score(self, loot):
        '''
        Increases the player's score.

        :param loot: amount of points to add
        '''
        self.score += loot

    def print_gold(self):
        '''
        Displays the player's gold on the screen.
        '''
        self.gold_text = self.myfont.render(str(self.gold), False, YELLOW)
        self.game.screen.blit(self.gold_text, (0, 0))

    def print_score(self):
        '''
        Displays the player's score on the screen.
        '''
        self.score_text = self.myfont.render(str(self.score), False, BLACK)
        self.game.screen.blit(self.score_text, (0, 30))
