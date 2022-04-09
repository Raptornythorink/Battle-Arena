import pygame

from ctypes import wintypes
from pygame.locals import *
from pygame.constants import K_SPACE

from Settings.settings import *
from SoundEffects.sounds import MenuSoundEffects
from Source.game import Game


mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Battle Arena - Start Menu")
screen = pygame.display.set_mode((WIDTH_MENU, HEIGHT_MENU), 0, 32)
screen_rect = screen.get_rect()

big_font = pygame.font.SysFont(FONT, 70)
medium_font = pygame.font.SysFont(FONT, 55)
small_font = pygame.font.SysFont(FONT, 40)


def draw_text_coords(text, font, color, surface, x, y):
    """
    Allows to draw text on a Pygame surface.
    :param text: the text to draw
    :param font: the font that has to be applied to the drawn text
    :param color: the color that has to be applied to the drawn text
    :param surface: the Pygame surface on which to draw the text
    :param x: x coordinate of the center of the rectangle that will contain the drawn text 
    :param y: y coordinate of the center of the rectangle that will contain the drawn text 
    """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def draw_text_in_surface(text, font, color, screen, surface):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = surface.center
    screen.blit(textobj, textrect)


def main_menu():
    """
    Opens a window displaying the main menu of the game. 
    """
    sound_effects = MenuSoundEffects()
    pygame.mixer.Sound.play(sound_effects.launch)
    playing_music = False
    start_music = sound_effects.launch.get_length() * 1000 + \
        pygame.time.get_ticks() + 100
    difficulty = 1
    pointing = 0
    running = True
    screen = pygame.display.set_mode((WIDTH_MENU, HEIGHT_MENU), 0, 32)

    while running:
        screen.fill(BLACK)
        if not playing_music and pygame.time.get_ticks() - start_music > 0:
            playing_music = True
            pygame.mixer.music.load(sound_effects.menu_music)
            pygame.mixer.music.play(-1)

        button_start = pygame.Rect(
            (WIDTH_MENU - WIDTH_BUTTON) // 2, 130, WIDTH_BUTTON, HEIGHT_BUTTON
        )
        button_option = pygame.Rect(
            (WIDTH_MENU - WIDTH_BUTTON) // 2, 300, WIDTH_BUTTON, HEIGHT_BUTTON
        )

        if pointing == 0:
            pygame.draw.rect(screen, WHITE, button_option)
            pygame.draw.rect(screen, RED, button_start)

        if pointing == 1:
            pygame.draw.rect(screen, RED, button_option)
            pygame.draw.rect(screen, WHITE, button_start)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return

                if event.key == K_UP or event.key == K_DOWN:
                    pointing = 1 - pointing
                    pygame.mixer.Sound.play(sound_effects.menu_cursor)
                if event.key == K_SPACE:
                    pygame.mixer.Sound.play(sound_effects.menu_select)
                    if pointing == 0:
                        pygame.mixer.music.stop()
                        battle_arena = Game()
                        battle_arena.new(difficulty)
                        battle_arena.run()

                        return
                    if pointing == 1:
                        difficulty = options()
                        pointing = 0

        draw_text_coords(
            "Battle-Arena", big_font, WHITE, screen, screen_rect.centerx, 60
        )
        draw_text_in_surface("Start", big_font, BLACK, screen, button_start)
        draw_text_in_surface("Options", big_font, BLACK, screen, button_option)
        draw_text_coords(
            "[Use arrows and spacebar]",
            small_font,
            ORANGE,
            screen,
            screen_rect.centerx,
            450,
        )
        pygame.display.update()
        mainClock.tick(60)


def options():
    """
    Displays the options menu.
    """
    sound_effects = MenuSoundEffects()
    vertical_pointing = 0
    horizontal_pointing = 1
    running = True

    while running:

        screen.fill(BLACK)

        button_easy = pygame.Rect(0, 130, WIDTH_MENU // 3, 100)
        button_medium = pygame.Rect(WIDTH_MENU // 3, 130, WIDTH_MENU // 3, 100)
        button_hard = pygame.Rect(2 * WIDTH_MENU // 3, 130, WIDTH_MENU // 3, 100)
        button_retour = pygame.Rect(
            screen_rect.centerx - WIDTH_BUTTON // 2, 300, WIDTH_BUTTON, HEIGHT_BUTTON
        )

        if vertical_pointing == 0:
            if horizontal_pointing == 0:
                pygame.draw.rect(screen, RED, button_easy)
                pygame.draw.rect(screen, WHITE, button_medium)
                pygame.draw.rect(screen, WHITE, button_hard)
            if horizontal_pointing == 1:
                pygame.draw.rect(screen, WHITE, button_easy)
                pygame.draw.rect(screen, RED, button_medium)
                pygame.draw.rect(screen, WHITE, button_hard)
            if horizontal_pointing == 2:
                pygame.draw.rect(screen, WHITE, button_easy)
                pygame.draw.rect(screen, WHITE, button_medium)
                pygame.draw.rect(screen, RED, button_hard)
            pygame.draw.rect(screen, WHITE, button_retour)

        if vertical_pointing == 1:
            pygame.draw.rect(screen, RED, button_retour)
            pygame.draw.rect(screen, WHITE, button_easy)
            pygame.draw.rect(screen, WHITE, button_medium)
            pygame.draw.rect(screen, WHITE, button_hard)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == K_UP or event.key == K_DOWN:
                    pygame.mixer.Sound.play(sound_effects.menu_cursor)
                    vertical_pointing = 1 - vertical_pointing
                if vertical_pointing == 0:
                    if event.key == K_LEFT and horizontal_pointing > 0:
                        horizontal_pointing -= 1
                        pygame.mixer.Sound.play(sound_effects.menu_cursor)
                    if event.key == K_RIGHT and horizontal_pointing < 2:
                        horizontal_pointing += 1
                        pygame.mixer.Sound.play(sound_effects.menu_cursor)
                if event.key == K_SPACE:
                    pygame.mixer.Sound.play(sound_effects.menu_select)
                    if vertical_pointing == 0:
                        return horizontal_pointing
                    if vertical_pointing == 1:
                        return 1

        draw_text_coords('Options', big_font, WHITE,
                         screen, screen_rect.centerx, 30)
        draw_text_coords('Difficulty', medium_font, WHITE,
                         screen, screen_rect.centerx, 100)
        draw_text_in_surface('Easy', big_font, BLACK, screen, button_easy)
        draw_text_in_surface('Medium', big_font, BLACK, screen, button_medium)
        draw_text_in_surface('Hard', big_font, BLACK, screen, button_hard)
        draw_text_in_surface('Back', big_font, BLACK, screen, button_retour)

        pygame.display.update()
        mainClock.tick(60)
