# For plugging in constants
import pygame

# Window
WIDTH = 720
HEIGHT = 720
TITLE = "Battle Arena"
TILESIZE = 32
FPS = 5
MAP_WIDTH = 800
MAP_HEIGHT = 800
FONT = pygame.font.get_default_font()

# Window menu
WIDTH_MENU = 600
HEIGHT_MENU = 500
WIDTH_BUTTON = 210
HEIGHT_BUTTON = 100

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
PURPLE = (102, 0, 153)
ORANGE = (237, 127, 16)
GOLD = (215, 215, 0)

# Player attributes
POS_PL_BASE = [3 * TILESIZE // 2, 3 * TILESIZE // 2]
HP_PL_BASE = 20
VIT_PL = 3
KB_PL_BASE = 50

# Weapon attributes
ATK_DMG = 5
ATK_RANGE = 100
KB_WP = 30
ATK_CD = 300  # cooldown between two consecutive attacks (in ms)

cost = {1: 5,
        2: 20, 3: 50, 4: 100, 5: 500,
        6: 10, 7: 60, 8: 150, 9: 500}
stats = {1: 5,  # buyable heal
         2: 5, 3: 15, 4: 40, 5: 100,  # leather, chainmail, iron, draconic armors
         6: 7, 7: 12, 8: 20, 9: 30}  # stick, dagger, scythe, sword weapons


# Ennemy attributes
mvt_acccy = 5  # à augmenter si des tremblements sont observés
ENEMY_STAT = {
    0: {
        "HP_ENEMY_BASE": 30,
        "HP_ENEMY_LOW": 7,
        "HP_ENEMY_HIGH": 30,
        "HP_ENEMY_BOSS": 100,
        "ATK_ENEMY_BASE": 2,
        "ATK_ENEMY_LOW": 1,
        "ATK_ENEMY_HIGH": 3,
        "VIT_ENEMY_BASE": 2,
        "VIT_ENEMY_LOW": 1,
        "VIT_ENEMY_HIGH": 4,
        "VIT_ENEMY_BOSS": 3,
        "KB_RES_BASE": 10,
        "KB_RES_LOW": 0,
        "KB_RES_HIGH": 30,
        "KB_RES_BOSS": 5,
        "LOOT_BASE": 10,
        "LOOT_LOW": 5,
        "LOOT_HIGH": 20,
        "LOOT_SUPER": 50,
    },
    1: {
        "HP_ENEMY_BASE": 45,
        "HP_ENEMY_LOW": 15,
        "HP_ENEMY_HIGH": 70,
        "HP_ENEMY_BOSS": 200,
        "ATK_ENEMY_BASE": 2,
        "ATK_ENEMY_LOW": 1,
        "ATK_ENEMY_HIGH": 5,
        "VIT_ENEMY_BASE": 2,
        "VIT_ENEMY_LOW": 1,
        "VIT_ENEMY_HIGH": 4,
        "VIT_ENEMY_BOSS": 3,
        "KB_RES_BASE": 10,
        "KB_RES_LOW": 0,
        "KB_RES_HIGH": 30,
        "KB_RES_BOSS": 5,
        "LOOT_BASE": 10,
        "LOOT_LOW": 5,
        "LOOT_HIGH": 20,
        "LOOT_SUPER": 50,
    },
    2: {
        "HP_ENEMY_BASE": 60,
        "HP_ENEMY_LOW": 20,
        "HP_ENEMY_HIGH": 150,
        "HP_ENEMY_BOSS": 450,
        "ATK_ENEMY_BASE": 3,
        "ATK_ENEMY_LOW": 2,
        "ATK_ENEMY_HIGH": 6,
        "VIT_ENEMY_BASE": 2,
        "VIT_ENEMY_LOW": 1,
        "VIT_ENEMY_HIGH": 4,
        "VIT_ENEMY_BOSS": 3,
        "KB_RES_BASE": 10,
        "KB_RES_LOW": 0,
        "KB_RES_HIGH": 30,
        "KB_RES_BOSS": 5,
        "LOOT_BASE": 10,
        "LOOT_LOW": 5,
        "LOOT_HIGH": 20,
        "LOOT_SUPER": 50,
    },
}

# Interface
PL_LIFEBAR_WIDTH = 500
PL_LIFEBAR_HEIGHT = 10
PL_LIFEBAR_OFFSET = 3
EN_LIFEBAR_HEIGHT = 5
EN_LIFEBAR_OFFSET = 10
ANTI_SPAWN_LENGTH = 64
FPS = 60

# Wave attribute
IND_BASE = 0
IND_RUSH = 1
IND_TANK = 2
IND_BOSS = 3

WAVE_ENEMIES = {
    0: [2, 0, 0, 0],
    1: [2, 0, 1, 0],
    2: [2, 1, 0, 0],
    3: [2, 1, 1, 0],
    4: [0, 0, 0, 1],
    5: [2, 2, 2, 0],
    6: [3, 2, 2, 0],
    7: [2, 2, 0, 1],
    8: [0, 4, 0, 0],
    9: [3, 0, 5, 0],
    10: [3, 0, 3, 1],
    11: [8, 0, 0, 0],
    12: [4, 2, 4, 0],
    13: [3, 0, 3, 2],
    14: [5, 2, 5, 0],
    15: [0, 8, 0, 0],
    16: [8, 4, 10, 3],
}  # 0=base enemy, 1=rush enemy, 2=tank enemy, 3=boss
WAVE_MAX = 16

WAVE_COOLDOWN = 5000

# Sprites

SPRITE_BACKGROUND = (64, 64, 192)
