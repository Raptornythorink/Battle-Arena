
from random import random

from Entities.entities import *
from Entities.lifebar import EnemyLifebar, EnemyLifebarOutline
from Settings.settings import *


class Wave:
    '''
    Allows to spawn a wave of ennemies.
    Once all of theme are dead, the shop opens.
    After that, the player has 5 seconds to recover before the next wave appears.

    :param game: the game instance that will contain the wave ennemies
    :param num: the number of the wave
    '''

    def __init__(self, game, num=0):
        self.num = num  # wave number
        self.game = game
        self.player_pos = self.game.player.pos
        self.wave_comp = WAVE_ENEMIES
        self.wave_over = False

        self.dic_enemy = {IND_BASE: BaseEnemy,
                          IND_RUSH: RushEnemy,
                          IND_TANK: TankEnemy,
                          IND_BOSS: BossEnemy}

    def enemies(self):
        """
        Creates and returns a list composed of self.num enemies to spawn.

        :returns: such a list
        """
        enemies = []
        actual_comp = self.wave_comp[self.num]
        for i in range(len(actual_comp)):
            for _ in range(actual_comp[i]):
                x = int((MAP_WIDTH - 2 * TILESIZE) * random()) + TILESIZE
                y = int((MAP_HEIGHT - 2 * TILESIZE) * random()) + TILESIZE
                while (
                    abs(x - self.player_pos[0]) <= ANTI_SPAWN_LENGTH
                    or abs(y - self.player_pos[1]) <= ANTI_SPAWN_LENGTH
                ):
                    x = int((MAP_WIDTH - 2 * TILESIZE) * random()) + TILESIZE
                    y = int((MAP_HEIGHT - 2 * TILESIZE) * random()) + TILESIZE
                enemy = self.dic_enemy[i](
                    self.game, [x, y], self.game.difficulty)
                enemies.append(enemy)
                self.game.enemy_lifebars_outline[enemy] = EnemyLifebarOutline(
                    enemy)
                self.game.enemy_lifebars[enemy] = EnemyLifebar(enemy)
        return enemies


    def next_wave(self):
        """
        Increments self.num by 1. If the final wave has been reached, triggers the winning process.
        """
        self.num += 1
        if self.num > WAVE_MAX:
            self.game.won()
        pygame.mixer.Sound.play(self.game.sound_effects.next_wave)

