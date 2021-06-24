import pytest
from factories import (
    GameFactory,
    MissionFactory,
    PlayerFactory
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def basic_game():
    return GameFactory.create(mission_set=MissionFactory.create_batch(10))


@pytest.fixture
def ongoing_game():
    game = GameFactory.create(mission_set=MissionFactory.create_batch(10))
    game.players.set(PlayerFactory.create_batch(5))
    game.start()
    return game


@pytest.fixture
def ready_config(client, ongoing_game):
    first_player = ongoing_game.players.first()
    client.cookies['player_id'] = first_player.id
    client.cookies['game_id'] = first_player.game.id
    return (client, ongoing_game, first_player)


def messages(resp):
    return [msg.message for msg in resp.context['messages']._loaded_messages]
