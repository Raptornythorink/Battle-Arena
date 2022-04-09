
import pygame

from random import choice


class MenuSoundEffects():
    '''
    Contains the references to the different sound files used in menus.
    '''
    def __init__(self):
        self.launch = pygame.mixer.Sound("SoundEffects/Sounds/LA_TitleAppear.wav")
        self.menu_cursor = pygame.mixer.Sound("SoundEffects/Sounds/LA_Menu_Cursor.wav")
        self.menu_select = pygame.mixer.Sound("SoundEffects/Sounds/LA_Menu_Select.wav")

        self.menu_music = "SoundEffects/Sounds/03 - Player Select.mp3"


class GameSoundEffects():
    '''
    Contains the references to the different sound files used in the game.
    '''
    def __init__(self):
        self.player_run = pygame.mixer.Sound("SoundEffects/Sounds/LA_Link_Run.wav")
        self.player_hurt = pygame.mixer.Sound("SoundEffects/Sounds/LA_Link_Hurt.wav")
        self.player_death = pygame.mixer.Sound("SoundEffects/Sounds/LA_Link_Dying.wav")

        self.sword_1 = pygame.mixer.Sound("SoundEffects/Sounds/LA_Sword_Slash1.wav")
        self.sword_2 = pygame.mixer.Sound("SoundEffects/Sounds/LA_Sword_Slash2.wav")
        self.sword_3 = pygame.mixer.Sound("SoundEffects/Sounds/LA_Sword_Slash3.wav")
        self.sword_4 = pygame.mixer.Sound("SoundEffects/Sounds/LA_Sword_Slash4.wav")
        self.sword_wall = pygame.mixer.Sound("SoundEffects/Sounds/LA_Sword_Tap.wav")

        self.enemy_hurt = pygame.mixer.Sound("SoundEffects/Sounds/LA_Enemy_Hit.wav")
        self.boss_hurt = pygame.mixer.Sound("SoundEffects/Sounds/LA_Enemy_Hit_Power.wav")
        self.enemy_dies = pygame.mixer.Sound("SoundEffects/Sounds/LA_Enemy_Die.wav")
        self.boss_dies = pygame.mixer.Sound("SoundEffects/Sounds/LA_Enemy_Die_Power.wav")

        self.heal = pygame.mixer.Sound("SoundEffects/Sounds/LA_Get_Item.wav")
        self.weapon_bought = pygame.mixer.Sound("SoundEffects/Sounds/LA_Fanfare_Item.wav")
        self.armor_bought = pygame.mixer.Sound("SoundEffects/Sounds/LA_Fanfare_HeartContainer.wav")

        self.next_wave = pygame.mixer.Sound("SoundEffects/Sounds/LA_Dungeon_Teleport.wav")
        self.win = pygame.mixer.Sound("SoundEffects/Sounds/LA_TrendyGame_Win.wav")

        self.main_music = "SoundEffects/Sounds/11 - Overworld.mp3"
        self.game_over = "SoundEffects/Sounds/79 - Game Over.mp3"
        self.game_won = "SoundEffects/Sounds/68 - Mt. Tamaranch.mp3"
    
    def play_sword_slash(self):
        '''
        Plays a random sword slash sound.
        '''
        SwordSlashSounds = [self.sword_1, self.sword_2, self.sword_3, self.sword_4]
        pygame.mixer.Sound.play(choice(SwordSlashSounds))




























