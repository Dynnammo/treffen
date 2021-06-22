from django import urls
from factories import PlayerFactory, MissionFactory, GameFactory
import pytest
from conftest import messages

pytestmark = pytest.mark.django_db


def test_waiting(client):
    player = PlayerFactory.create()
    client.cookies['player_id'] = player.id
    client.cookies['game_id'] = player.game.id
    url = urls.reverse('waiting_page')
    resp = client.get(url)

    assert resp.status_code == 200
    assert player in resp.context_data.values()


def test_waiting_not_enough_players(client, basic_game):
    p = PlayerFactory.create(game=basic_game)
    client.cookies['player_id'] = p.id
    client.cookies['game_id'] = p.game.id
    url = urls.reverse('waiting_page')
    resp = client.get(url)

    basic_game.status = basic_game.STARTED
    basic_game.save()

    assert messages(resp)[0].message == 'Game has not started yet'
    assert messages(resp)[0].level_tag == 'error'
    assert resp.status_code == 200
    assert p.game.status == basic_game.WAITING_TO_START


def test_waiting_not_enough_missions(client):
    game = GameFactory.create(mission_set=MissionFactory.create_batch(1))
    game.players.set(PlayerFactory.create_batch(10))
    p = game.players.first()
    client.cookies['player_id'] = p.id
    client.cookies['game_id'] = p.game.id

    game.status = game.STARTED
    game.save()

    url = urls.reverse('waiting_page')
    resp = client.get(url)

    assert messages(resp)[0].message == 'Game has not started yet'
    assert messages(resp)[0].level_tag == 'error'
    assert resp.status_code == 200
    assert p.game.status == game.WAITING_TO_START


def test_waiting_game_has_started(client):
    game = GameFactory.create(mission_set=MissionFactory.create_batch(10))
    game.players.set(PlayerFactory.create_batch(5))
    p = game.players.first()
    client.cookies['player_id'] = p.id
    client.cookies['game_id'] = p.game.id

    game.status = game.STARTED
    game.save()

    url = urls.reverse('waiting_page')
    resp = client.get(url)

    assert resp.status_code == 302
    assert p.game.status == game.STARTED

    url = urls.reverse(resp.url[1:])
    resp = client.get(url)
    assert resp.status_code == 200
    assert messages(resp)[0].message == 'Game has just started!'
