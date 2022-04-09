
import pygame

from pygame.constants import K_SPACE
from pygame.locals import *

from Settings.settings import *
from SoundEffects.sounds import MenuSoundEffects


pygame.init()

font = pygame.font.SysFont(pygame.font.get_default_font(), 70)
font2 = pygame.font.SysFont(pygame.font.get_default_font(), 40)


def draw_text(text, font, color, surface, x, y):
    '''
    Writes text on a pygame surface.

    :param text: the text to write
    :param font: the font to be applied to the text
    :param color: the color to be applied to the text
    :param x: x coordinate of the top left corner of the rectangle containing the text
    :param y: y coordinate of the top left corner of the rectangle containing the text
    '''
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def buy(game, pointer):
    '''
    Allows to buy an item.

    :param game: the game instance
    :param pointer: the index number of the item to buy
    '''
    if game.item_available[pointer] and cost[pointer] <= game.player.gold:
        if pointer == 1:
            if game.player.hp < game.player.hp_max:
                game.player.heal(5)
                pygame.mixer.Sound.play(game.sound_effects.heal)
                game.player.gold -= cost[pointer]

        elif pointer < 6:
            hpm = game.player.hp_max
            pygame.mixer.Sound.play(game.sound_effects.armor_bought)
            for i in range(2, pointer + 1):
                game.item_available[i] = False

            game.player.hp_max = game.player.hp_max + stats[pointer]

            game.player.hp = game.player.hp * game.player.hp_max // hpm
            game.player.gold -= cost[pointer]

        else:
            game.weapon.atk = max(game.weapon.atk, stats[pointer])
            pygame.mixer.Sound.play(game.sound_effects.weapon_bought)
            for i in range(6, pointer + 1):
                game.item_available[i] = False
            game.player.gold -= cost[pointer]


def interwave_menu(game):
    '''
    Displays an interactive menu between two consecutive waves,
    allowing the player to buy healing, weapons and armors.

    :param game: the game instance
    '''
    sound_effects = MenuSoundEffects()
    mainClock = game.clock
    mainClock.tick(2)
    pas_x = WIDTH / 100
    pas_y = HEIGHT / 100
    _screen = game.screen
    pointing = 1
    pointing_side = [-1, 1, 6, 7, 8, 9, 2, 3, 4, 5]
    pointing_down = [-1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    pointing_up = [-1, 9, 1, 2, 3, 4, 1, 6, 7, 8]
    pointing_lefttop = [
        0,
        (32 * pas_x, 15 * pas_y),
        (12 * pas_x, (15 + 12 + 5) * pas_y),
        (12 * pas_x, (15 + 2 * 12 + 2 * 5) * pas_y),
        (12 * pas_x, (15 + 3 * 12 + 3 * 5) * pas_y),
        (12 * pas_x, (15 + 4 * 12 + 4 * 5) * pas_y),
        (57 * pas_x, (15 + 12 + 5) * pas_y),
        (57 * pas_x, (15 + 2 * 12 + 2 * 5) * pas_y),
        (57 * pas_x, (15 + 3 * 12 + 3 * 5) * pas_y),
        (57 * pas_x, (15 + 4 * 12 + 4 * 5) * pas_y),
    ]

    while True:
        _screen.fill((249, 216, 131))
        # left top width height
        button_10 = pygame.Rect(
            pointing_lefttop[pointing][0],
            pointing_lefttop[pointing][1],
            36 * pas_x,
            12 * pas_y,
        )  # 'encadrement'
        button_1 = pygame.Rect(32 * pas_x, 15 * pas_y,
                               36 * pas_x, 12 * pas_y)  # 'soin'
        button_2 = pygame.Rect(
            12 * pas_x, (15 + 12 + 5) * pas_y, 36 * pas_x, 12 * pas_y
        )  # 'armure 1'
        button_3 = pygame.Rect(
            12 * pas_x, (15 + 2 * 12 + 2 * 5) * pas_y, 36 * pas_x, 12 * pas_y
        )  # 'armure 2'
        button_4 = pygame.Rect(
            12 * pas_x, (15 + 3 * 12 + 3 * 5) * pas_y, 36 * pas_x, 12 * pas_y
        )  # 'armure 3'
        button_5 = pygame.Rect(
            12 * pas_x, (15 + 4 * 12 + 4 * 5) * pas_y, 36 * pas_x, 12 * pas_y
        )  # 'armure 4'

        button_6 = pygame.Rect(
            57 * pas_x, (15 + 12 + 5) * pas_y, 36 * pas_x, 12 * pas_y
        )  # 'arme 1'
        button_7 = pygame.Rect(
            57 * pas_x, (15 + 2 * 12 + 2 * 5) * pas_y, 36 * pas_x, 12 * pas_y
        )  # 'arme 2'
        button_8 = pygame.Rect(
            57 * pas_x, (15 + 3 * 12 + 3 * 5) * pas_y, 36 * pas_x, 12 * pas_y
        )  # 'arme 3'
        button_9 = pygame.Rect(
            57 * pas_x, (15 + 4 * 12 + 4 * 5) * pas_y, 36 * pas_x, 12 * pas_y
        )  # 'arme 3'

        buttons = [
            button_10,
            button_1,
            button_2,
            button_3,
            button_4,
            button_5,
            button_6,
            button_7,
            button_8,
            button_9,
        ]

        for button in buttons:
            if button == button_10:
                pygame.draw.rect(_screen, RED, button, width=3)
            if button != button_10:
                pygame.draw.rect(_screen, WHITE, button)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == K_LEFT or event.key == K_RIGHT:
                    pointing = pointing_side[pointing]
                    pygame.mixer.Sound.play(sound_effects.menu_cursor)
                if event.key == K_UP:
                    pointing = pointing_up[pointing]
                    pygame.mixer.Sound.play(sound_effects.menu_cursor)
                if event.key == K_DOWN:
                    pointing = pointing_down[pointing]
                    pygame.mixer.Sound.play(sound_effects.menu_cursor)
                if event.key == K_RETURN:
                    game.inmenu = False
                    game.wave_time = pygame.time.get_ticks()
                    game.wave.wave_over = True
                    game.lifebar_player.update_lifebar()
                    game.run()
                if event.key == K_SPACE:
                    buy(game, pointing)

        text_colors = [BLACK] * (len(cost) + 1)
        for i in range(len(cost)):
            if not game.item_available[i + 1]:
                text_colors[i + 1] = RED
        if game.player.hp == game.player.hp_max:
            text_colors[1] = RED

        draw_text(
            "Shop - SPACEBAR to buy and ENTER to play ",
            font2,
            ORANGE,
            _screen,
            7 * pas_x,
            7 * pas_y,
        )

        draw_text("Heal 5 hp", font2, (0, 130, 0),
                  _screen, 40 * pas_x, 17 * pas_y)
        draw_text(
            "Cost: " + str(cost[1]),
            font2,
            (255 * (cost[1] > game.player.gold or
            game.player.hp == game.player.hp_max), 0, 0),
            _screen,
            40 * pas_x,
            21 * pas_y,
        )

        draw_text("Current gold", font2, RED, _screen, 69 * pas_x, 15 * pas_y)
        draw_text(
            "amount: " + str(game.player.gold),
            font2,
            WHITE,
            _screen,
            69 * pas_x,
            19 * pas_y,
        )

        draw_text("Current stats:", font2, RED, _screen, 1 * pas_x, 14 * pas_y)
        draw_text(
            "HP: " + str(game.player.hp) + "/" + str(game.player.hp_max),
            font2,
            WHITE,
            _screen,
            5 * pas_x,
            18 * pas_y,
        )
        draw_text(
            "ATK: " + str(game.weapon.atk), font2, WHITE, _screen, 5 *
            pas_x, 22 * pas_y
        )

        draw_text(
            "Leather: +" + str(stats[2]) + "HP",
            font2,
            text_colors[2],
            _screen,
            15 * pas_x,
            33 * pas_y,
        )
        draw_text(
            "Cost: " + str(cost[2]),
            font2,
            (255 * (cost[2] > game.player.gold
            or not game.item_available[2]), 0, 0),
            _screen,
            17 * pas_x,
            38 * pas_y,
        )

        draw_text(
            "Chainmail: +" + str(stats[3]) + "HP",
            font2,
            text_colors[3],
            _screen,
            13 * pas_x,
            (33 + 17) * pas_y,
        )
        draw_text(
            "Cost: " + str(cost[3]),
            font2,
            (255 * (cost[3] > game.player.gold
            or not game.item_available[3]), 0, 0),
            _screen,
            17 * pas_x,
            (38 + 17) * pas_y,
        )

        draw_text(
            "Iron plates: +" + str(stats[4]) + "HP",
            font2,
            text_colors[4],
            _screen,
            13 * pas_x,
            (33 + 2 * 17) * pas_y,
        )
        draw_text(
            "Cost: " + str(cost[4]),
            font2,
            (255 * (cost[4] > game.player.gold
            or not game.item_available[4]), 0, 0),
            _screen,
            17 * pas_x,
            (38 + 2 * 17) * pas_y,
        )

        draw_text(
            "Draconic: +" + str(stats[5]) + "HP",
            font2,
            text_colors[5],
            _screen,
            13 * pas_x,
            (33 + 3 * 17) * pas_y,
        )
        draw_text(
            "Cost: " + str(cost[5]),
            font2,
            (255 * (cost[5] > game.player.gold
            or not game.item_available[5]), 0, 0),
            _screen,
            17 * pas_x,
            (38 + 3 * 17) * pas_y,
        )

        draw_text(
            "Stick: " + str(stats[6]) + " ATK",
            font2,
            text_colors[6],
            _screen,
            (45 + 17) * pas_x,
            33 * pas_y,
        )
        draw_text(
            "Cost: " + str(cost[6]),
            font2,
            (255 * (cost[6] > game.player.gold
            or not game.item_available[6]), 0, 0),
            _screen,
            (45 + 17) * pas_x,
            38 * pas_y,
        )

        draw_text(
            "Dagger: " + str(stats[7]) + " ATK",
            font2,
            text_colors[7],
            _screen,
            (45 + 17) * pas_x,
            (17 + 33) * pas_y,
        )
        draw_text(
            "Cost: " + str(cost[7]),
            font2,
            (255 * (cost[7] > game.player.gold
            or not game.item_available[7]), 0, 0),
            _screen,
            (45 + 17) * pas_x,
            (17 + 38) * pas_y,
        )

        draw_text(
            "Scythe: " + str(stats[8]) + " ATK",
            font2,
            text_colors[8],
            _screen,
            (45 + 17) * pas_x,
            (2 * 17 + 33) * pas_y,
        )
        draw_text(
            "Cost: " + str(cost[8]),
            font2,
            (255 * (cost[8] > game.player.gold
            or not game.item_available[8]), 0, 0),
            _screen,
            (45 + 17) * pas_x,
            (2 * 17 + 38) * pas_y,
        )

        draw_text(
            "Sword: " + str(stats[9]) + " ATK",
            font2,
            text_colors[9],
            _screen,
            (45 + 17) * pas_x,
            (3 * 17 + 33) * pas_y,
        )
        draw_text(
            "Cost: " + str(cost[9]),
            font2,
            (255 * (cost[9] > game.player.gold
            or not game.item_available[9]), 0, 0),
            _screen,
            (45 + 17) * pas_x,
            (3 * 17 + 38) * pas_y,
        )

        pygame.display.update()
        mainClock.tick(60)


def menu_game_over(game):
    '''
    Displays a Game Over screen with the player's score and maximum wave.

    :param game: the game instance that is coming to and end
    '''
    screen = game.screen
    screen.fill(BLACK)

    font1 = pygame.font.SysFont(FONT, 120)
    font2 = pygame.font.SysFont(FONT, 90)
    font3 = pygame.font.SysFont(FONT, 90)

    text_object_1 = font1.render("GAME  OVER", 1, RED)
    text_object_score = font2.render(
        "Score : " + str(game.player.score), 1, WHITE)
    text_object_wave = font3.render("Wave : " + str(game.wave.num+1), 1, WHITE)

    text_object_1_rect = text_object_1.get_rect()
    text_object_score_rect = text_object_score.get_rect()
    text_object_wave_rect = text_object_wave.get_rect()

    text_object_1_rect.center = (WIDTH // 2, HEIGHT // 3)
    text_object_score_rect.center = (WIDTH // 2, 2 * HEIGHT // 4)
    text_object_wave_rect.center = (WIDTH // 2, 3 * HEIGHT // 4)

    pygame.mixer.Sound.play(game.sound_effects.player_death)
    playing_music = False
    start_music = (
        game.sound_effects.player_death.get_length() * 1000
        + pygame.time.get_ticks()
        + 100
    )
    while True:
        if not playing_music and pygame.time.get_ticks() - start_music > 0:
            playing_music = True
            pygame.mixer.music.load(game.sound_effects.game_over)
            pygame.mixer.music.play(-1)
        screen.blit(text_object_1, text_object_1_rect)
        screen.blit(text_object_score, text_object_score_rect)
        screen.blit(text_object_wave, text_object_wave_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return
        pygame.display.update()


def menu_victory(game):
    '''
    Displays a Victory screen with the player's score.

    :param game: the game instance that is coming to and end
    '''
    screen = game.screen
    pygame.mixer.Sound.play(game.sound_effects.win)
    screen.fill(BLACK)
    font1 = pygame.font.SysFont(FONT, 120)
    font2 = pygame.font.SysFont(FONT, 90)
    text_object_1 = font1.render("VICTORY !", 1, RED)
    text_object_score = font2.render(
        "Score : " + str(game.player.score), 1, WHITE)
    text_object_1_rect = text_object_1.get_rect()
    text_object_score_rect = text_object_score.get_rect()
    text_object_1_rect.center = (WIDTH // 2, HEIGHT // 3)
    text_object_score_rect.center = (WIDTH // 2, 2 * HEIGHT // 3)
    playing_music = False
    start_music = (
        game.sound_effects.win.get_length() * 1000 + pygame.time.get_ticks() + 100
    )
    while True:
        if not playing_music and pygame.time.get_ticks() - start_music > 0:
            playing_music = True
            pygame.mixer.music.load(game.sound_effects.game_won)
            pygame.mixer.music.play(-1)
        screen.blit(text_object_1, text_object_1_rect)
        screen.blit(text_object_score, text_object_score_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return
        pygame.display.update()
