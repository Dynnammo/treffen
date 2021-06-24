from django import urls
from conftest import messages
import pytest

pytestmark = pytest.mark.django_db


def test_eliminate_ziel_code_is_wrong(ready_config):
    client, game, player = ready_config
    url = urls.reverse('game')
    posting_data = {'player_code': str(int(player.ziel.player_code) + 1)}
    resp = client.post(url, posting_data)

    assert resp.status_code == 302

    resp = client.get(urls.reverse(resp.url))
    assert messages(resp)[0].message == 'The code you have entered is wrong 😠'


def test_eliminate_ziel_but_player_was_eliminated(ready_config):
    client, game, player = ready_config
    ziel = player.ziel
    ziel_of_ziel = ziel.ziel

    # Eliminate player
    url = urls.reverse('game')
    posting_data = {'player_code': ziel.player_code}
    client.post(url, posting_data)
    ziel.refresh_from_db()
    assert ziel.status == ziel.IS_OUT

    # Ziel tries to eliminate player
    client.cookies['player_id'] = ziel.id
    client.cookies['game_id'] = game.id
    posting_data = {'player_code': ziel_of_ziel.player_code}
    resp = client.post(url, posting_data)
    assert resp.status_code == 302
    assert resp.url == '/end_game'

    #  TODO: determine why there is 2 messages instead of 1
    resp = client.get(urls.reverse(resp.url[1:]))
    ziel_of_ziel.refresh_from_db()
    assert messages(resp)[1].message == 'You are out of the game'
    assert ziel_of_ziel.status == ziel_of_ziel.IS_PLAYING


def test_eliminate_ziel_all_correct(ready_config):
    client, _, player = ready_config
    url = urls.reverse('game')
    posting_data = {'player_code': player.ziel.player_code}
    resp = client.post(url, posting_data)

    assert resp.status_code == 302

    resp = client.get(urls.reverse(resp.url))
    assert messages(resp)[0].message == 'Good job ! Here is your new ziel!'


def test_game_is_over_player_has_won(ready_config):
    client, game, player = ready_config
    game.status = game.OVER
    game.save()

    url = urls.reverse('game')
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == '/end_game'

    resp = client.get(urls.reverse(resp.url[1:]))
    assert resp.status_code == 200
    assert messages(resp)[0].message == 'You have won the game'


def test_game_is_over_player_has_lost(ready_config):
    client, game, player = ready_config
    game.status = game.OVER
    game.save()

    player.ziel = None
    player.save()

    url = urls.reverse('game')
    resp = client.get(url)
    assert resp.status_code == 302
    assert resp.url == '/end_game'

    resp = client.get(urls.reverse(resp.url[1:]))
    assert resp.status_code == 200
    assert messages(resp)[0].message == 'You are out of the game'
