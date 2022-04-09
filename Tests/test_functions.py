
from battle_arena import *
from Entities.entities import *
from Entities.player import *
from Entities.player_model import *
from Settings.settings import *


def test_enemy():
    game = Game()
    game.new()
    enemy = Enemy(game, [300, 200], 300, 0.4)

    enemy.move_enemy()
    assert enemy.pos == [299, 199]
    enemy.player_pos = [400, 400]

    enemy.move_enemy()
    assert enemy.pos == [300, 200]

    enemy.move_enemy()
    assert enemy.pos == [301, 201]


def test_hurt():
    game = Game()
    game.new()
    player = game.player
    hp = player.hp

    player.hurt(10)

    assert player.hp == hp - 10


def test_heal():
    game = Game()
    game.new()
    player = game.player
    hp = player.hp

    player.hurt(10)
    player.heal(5)

    assert player.hp == hp - 5

    player.heal(20)

    assert player.hp == hp


def test_wave_ennemies():
    game = Game()
    game.new()

    for i in range(0, WAVE_MAX + 1):
        wave = Wave(game, i)
        ennemies = wave.enemies()

        s = 0
        for x in WAVE_ENEMIES[i]:
            s += x

        assert len(ennemies) == s


def test_next_wave():
    game = Game()
    game.new()

    wave = Wave(game, 2)
    wave.next_wave()

    assert wave.num == 3


def test_player_move():
    game = Game()
    player = Player(game, [MAP_WIDTH // 2, MAP_HEIGHT // 2])
    player.move(-1, 0)
    assert player.pos == [MAP_WIDTH // 2 - player.vitesse, MAP_WIDTH // 2]

    game = Game()
    player = Player(game, [MAP_WIDTH // 2, MAP_HEIGHT // 2])
    player.move(1, 0)
    assert player.pos == [MAP_WIDTH // 2 + player.vitesse, MAP_WIDTH // 2]

    game = Game()
    player = Player(game, [MAP_WIDTH // 2, MAP_HEIGHT // 2])
    player.move(0, -1)
    assert player.pos == [MAP_WIDTH // 2, MAP_WIDTH // 2 - player.vitesse]

    game = Game()
    player = Player(game, [MAP_WIDTH // 2, MAP_HEIGHT // 2])
    player.move(0, 1)
    assert player.pos == [MAP_WIDTH // 2, MAP_WIDTH // 2 + player.vitesse]


def test_player_facing():
    game = Game()
    player = Player(game, [MAP_WIDTH // 2, MAP_HEIGHT // 2])

    for dir in ["left", "right", "up", "down"]:
        player.update_pl_facing(dir)
        assert player.facing == dir


def test_player_model_move():
    game = Game()
    game.new()
    player_model = PlayerModel(game)
    pos = player_model.rect.x, player_model.rect.y
    game.player.move(-1, 0)
    player_model.update_pos()
    assert player_model.rect.x == pos[0] - game.player.vitesse
    
    game = Game()
    game.new()
    player_model = PlayerModel(game)
    pos = player_model.rect.x, player_model.rect.y
    game.player.move(0, 1)
    player_model.update_pos()
    assert player_model.rect.y == pos[1] + game.player.vitesse
