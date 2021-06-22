from django import urls
from factories import PlayerFactory
from treffen.models import Player
import pytest

pytestmark = pytest.mark.django_db


def test_registration(client):
    url = urls.reverse('registration')
    resp = client.get(url)

    assert resp.status_code == 200


def test_form_game_not_valid(client, basic_game):
    player = PlayerFactory.build(game=basic_game)
    player_data = {
        'name': player.name,
        'picture': player.picture,
        'game_name': player.game.name + "XXX"
    }

    url = urls.reverse('registration')
    resp = client.post(url, player_data)

    errors = resp.context_data['form'].errors
    assert len(errors) != 0
    assert errors['Invalid game']


def test_form_invalid_registration(client, basic_game):
    player = PlayerFactory.build(game=basic_game)
    player_data = {
        'game_name': player.game.name
    }

    url = urls.reverse('registration')
    resp = client.post(url, player_data)

    errors = resp.context_data['form'].errors
    assert len(errors) != 0
    assert errors['Invalid identification']


def test_form_valid(client, basic_game):
    initial_count = Player.objects.count()
    player = PlayerFactory.build(game=basic_game)
    player_data = {
        'name': player.name,
        'picture': player.picture,
        'game_name': player.game.name
    }

    url = urls.reverse('registration')
    resp = client.post(url, player_data)

    assert Player.objects.count() == initial_count + 1
    assert resp.cookies['player_id']
    assert resp.status_code == 302
    assert resp.url == "waiting"
