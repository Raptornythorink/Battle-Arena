
from Entities.entities import *
from Settings.settings import *


class PlayerLifebarOutline(pygame.sprite.Sprite):
    '''
    Red unchanging lifebar for the player, displayed at the top of the screen.

    :param game: the game instance on which to display the lifebar
    '''
    def __init__(self, game):
        self.game = game

        pygame.sprite.Sprite.__init__(self)
        self.game.all_sprites_window.add(self)
        self.image = pygame.Surface([PL_LIFEBAR_WIDTH, PL_LIFEBAR_HEIGHT])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH // 2, PL_LIFEBAR_OFFSET + PL_LIFEBAR_HEIGHT // 2]


class PlayerLifebar(pygame.sprite.Sprite):
    '''
    Green dynamic lifebar for the player, displayed at the top of the screen.
    Its length changes according to the player's hp.

    :param game: the game instance on which to display the lifebar
    '''
    def __init__(self, game):
        self.game = game

        pygame.sprite.Sprite.__init__(self)
        self.game.all_sprites_window.add(self)
        self.image = pygame.Surface([PL_LIFEBAR_WIDTH, PL_LIFEBAR_HEIGHT])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH // 2, PL_LIFEBAR_OFFSET + PL_LIFEBAR_HEIGHT // 2]
    
    def update_lifebar(self):
        '''
        Updates the player's green lifebar by rescaling it.
        '''
        self.image =pygame.transform.scale(self.image,
                               [PL_LIFEBAR_WIDTH * max(0, self.game.player.hp) // self.game.player.hp_max, PL_LIFEBAR_HEIGHT])


class EnemyLifebarOutline(pygame.sprite.Sprite):
    '''
    Red unchanging lifebar for an enemy, displayed slightly over
    said enemy and moving along with them.

    :param enemy: the enemy attached to the lifebar
    '''

    def __init__(self, enemy):
        self.enemy = enemy
        self.game = enemy.game

        pygame.sprite.Sprite.__init__(self)
        self.game.all_sprites.add(self)
        self.image = pygame.Surface([self.enemy.hp_max, EN_LIFEBAR_HEIGHT])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = [self.enemy.pos[0], self.enemy.pos[1] - TILESIZE // 2 - EN_LIFEBAR_OFFSET]
    
    def move(self):
        '''
        Moves the enemy's red lifebar according to the enemy's position.
        '''
        self.rect.center = [self.enemy.pos[0], self.enemy.pos[1] - TILESIZE // 2 - EN_LIFEBAR_OFFSET]


class EnemyLifebar(pygame.sprite.Sprite):
    '''
    Green dynamic lifebar for an enemy, displayed slightly over said enemy
    and moving along with them. Its length depends on the enemy's hp.

    :param enemy: the enemy attached to the lifebar
    '''
    def __init__(self, enemy):
        self.enemy = enemy
        self.game = self.enemy.game

        pygame.sprite.Sprite.__init__(self)
        self.game.all_sprites.add(self)
        self.image = pygame.Surface([self.enemy.hp_max, EN_LIFEBAR_HEIGHT])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = [self.enemy.pos[0], self.enemy.pos[1] - TILESIZE // 2 - EN_LIFEBAR_OFFSET]
    
    def move(self):
        '''
        Moves the enemy's green lifebar according to the enemy's position.
        '''
        self.rect.center = [self.enemy.pos[0], self.enemy.pos[1] - TILESIZE // 2 - EN_LIFEBAR_OFFSET]
    
    def update_lifebar(self):
        '''
        Updates the enemy's green lifebar by rescaling it.
        '''
        self.image = pygame.transform.scale(self.image,
                               [max(0, self.enemy.hp), EN_LIFEBAR_HEIGHT])

