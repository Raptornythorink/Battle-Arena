
import pygame
import pyscroll
import pytmx

from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP
from pygame.locals import *

from Menus.shop_and_end_screens import interwave_menu, menu_game_over, menu_victory
from Entities.entities import *
from Entities.lifebar import *
from Entities.player import *
from Entities.player_model import *
from Entities.weapons import *
from Entities.spritesheet import *
from Settings.settings import *
from SoundEffects.sounds import GameSoundEffects
from Source.waves import *


class Game:
    '''
    Defines a game session, handling the screen and the different entities.
    '''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.sound_effects = GameSoundEffects()

        self.tmx_data = pytmx.load_pygame("Textures/map_tiled.tmx", pixelalpha=True)
        self.map_data = pyscroll.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(
            self.map_data, (WIDTH, HEIGHT))
        self.map_layer.zoom = 1.2

    def new(self, difficulty=1):
        """
        Creation of the entities.

        :param difficulty: the difficulty to apply to the enemies's stats
        """
        self.inmenu = False
        self.all_sprites = pyscroll.PyscrollGroup(
            map_layer=self.map_layer)
        self.all_sprites_window = pygame.sprite.Group()
        self.difficulty = difficulty
        self.player = Player(self, (POS_PL_BASE))
        self.player_model = PlayerModel(self)
        self.wave = Wave(self)

        self.item_available = [True] * (len(cost) + 1) # displays whether or not a shop item has been bought

        self.enemy_lifebars_outline = {}
        self.enemy_lifebars = {}

        pygame.mixer.music.load(self.sound_effects.main_music)
        pygame.mixer.music.play(-1)

        self.enemies = self.wave.enemies()

        self.walls = [
            Wall(self, "up", 0, MAP_WIDTH, -TILESIZE // 2, TILESIZE // 2),
            Wall(self, "down", 0, MAP_WIDTH, MAP_HEIGHT -
                 TILESIZE // 2, MAP_HEIGHT + TILESIZE // 2),
            Wall(self, "left", -TILESIZE // 2, TILESIZE // 2, 0, MAP_HEIGHT),
            Wall(self, "right", MAP_WIDTH - TILESIZE // 2,
                 MAP_WIDTH + TILESIZE // 2, 0, MAP_HEIGHT),
        ]

        self.weapon = Weapon(self)

        self.lifebar_player_outline = PlayerLifebarOutline(self)
        self.lifebar_player = PlayerLifebar(self)

    def run(self):
        """
        Main loop.
        """
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def events(self):
        """
        Handles pygame events.
        """
        for event in pygame.event.get():
            # Closing the window
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Attacking with space bar
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                self.player.attack()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_ESCAPE]:
            pygame.quit()
            return

        # Moving the player if the arrows keys are pressed
        if keys_pressed[K_LEFT]:
            # update animation
            current_time = pygame.time.get_ticks()
            if (
                current_time - self.player_model.last_update
                > self.player_model.animation_cooldown
            ):
                self.player_model.frame = (
                    self.player_model.frame + 1
                ) % self.player_model.animation_steps
                self.player_model.last_update = current_time
                self.player_model.image = self.player_model.animation_list_left[
                    self.player_model.frame]

            if keys_pressed[K_DOWN]:
                self.player.move(-1, 1)
            elif keys_pressed[K_UP]:
                self.player.move(-1, -1)
            else:
                self.player.move(-1, 0)
            self.player.update_pl_facing("left")

        if keys_pressed[K_RIGHT]:
            current_time = pygame.time.get_ticks()
            if (
                current_time - self.player_model.last_update
                > self.player_model.animation_cooldown
            ):
                self.player_model.frame = (
                    self.player_model.frame + 1
                ) % self.player_model.animation_steps
                self.player_model.last_update = current_time
                self.player_model.image = self.player_model.animation_list_right[
                    self.player_model.frame]

            if keys_pressed[K_DOWN]:
                self.player.move(1, 1)
            elif keys_pressed[K_UP]:
                self.player.move(1, -1)
            else:
                self.player.move(1, 0)
            self.player.update_pl_facing("right")
        if (
            keys_pressed[K_UP]
            and not keys_pressed[K_RIGHT]
            and not keys_pressed[K_LEFT]
        ):
            self.player.move(0, -1)
            self.player.update_pl_facing("up")
            current_time = pygame.time.get_ticks()
            if (
                current_time - self.player_model.last_update
                > self.player_model.animation_cooldown
            ):
                self.player_model.frame = (
                    self.player_model.frame + 1
                ) % self.player_model.animation_steps
                self.player_model.last_update = current_time
                self.player_model.image = self.player_model.animation_list_up[
                    self.player_model.frame]
        if (
            keys_pressed[K_DOWN]
            and not keys_pressed[K_RIGHT]
            and not keys_pressed[K_LEFT]
        ):
            self.player.move(0, 1)
            self.player.update_pl_facing("down")
            current_time = pygame.time.get_ticks()
            if (
                current_time - self.player_model.last_update
                > self.player_model.animation_cooldown
            ):
                self.player_model.frame = (
                    self.player_model.frame + 1
                ) % self.player_model.animation_steps
                self.player_model.last_update = current_time
                self.player_model.image = self.player_model.animation_list_down[
                    self.player_model.frame]


    def update(self):
        """
        Updates the entities' data.
        """
        if self.inmenu:
            interwave_menu(self)

        if not self.inmenu:
            if not self.enemies:
                if not self.wave.wave_over:
                    self.inmenu = True

                if (
                    self.wave.wave_over
                    and pygame.time.get_ticks() - self.wave_time > WAVE_COOLDOWN
                ):
                    self.wave.next_wave()
                    self.enemies = self.wave.enemies()
                    self.wave.wave_over = False

        for enemy in self.enemies:
            current_time = pygame.time.get_ticks()
            if current_time - enemy.last_update > enemy.animation_cooldown:
                enemy.frame = (enemy.frame + 1) % enemy.animation_steps
                enemy.last_update = current_time
                enemy.image = enemy.animation_list[enemy.frame]
            if pygame.sprite.spritecollideany(self.player, [enemy]):
                enemy.knockbacks_enemy_player(self.player.kb)
                self.player.hurt(enemy.atk)
            if enemy.hp <= 0:
                self.player.add_gold(enemy.loot)
                self.player.add_score(enemy.loot)
                self.enemies.remove(enemy)
                self.enemy_lifebars_outline[enemy].kill()
                self.enemy_lifebars_outline.pop(enemy)
                self.enemy_lifebars[enemy].kill()
                self.enemy_lifebars.pop(enemy)
                enemy.kill()
                enemy.kill()
                pygame.mixer.Sound.play(self.sound_effects.enemy_dies)
            else:
                for wall in self.walls:
                    if pygame.sprite.spritecollideany(enemy, [wall]):
                        wall.knockbacks_enemy(enemy)
                enemy.update_enemy()
        for wall in self.walls:
            if pygame.sprite.spritecollideany(self.player, [wall]):
                wall.knockbacks_player()
            if self.weapon.animation and not self.weapon.playing_wall_tap and (
                    pygame.sprite.spritecollideany(self.weapon, [wall])):
                pygame.mixer.Sound.play(self.sound_effects.sword_wall)
                self.weapon.playing_wall_tap = True
        self.weapon.update_weapon()
        self.player_model.update_pos()

    def draw(self):
        """
        Displays the different sprites on the screen.
        """
        self.all_sprites.center(self.player.rect.center)
        self.all_sprites.draw(self.screen)
        self.all_sprites_window.draw(self.screen)
        self.player.print_gold()
        self.player.print_score()
        pygame.display.update()

    def quit(self):
        """
        Stops the program.
        """
        pygame.quit()
        return

    def lost(self):
        """
        Handles the defeat of a game by closing the window and printing a message.
        """
        self.running = False
        pygame.mixer.music.stop()
        menu_game_over(self)

    def won(self):
        """
        Handles the victory of a game by closing the window and printing a message.
        """
        self.running = False
        pygame.mixer.music.stop()
        menu_victory(self)
