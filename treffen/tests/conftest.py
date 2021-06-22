import pytest
from factories import (
    GameFactory,
    MissionFactory
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def basic_game():
    return GameFactory.create(mission_set=MissionFactory.create_batch(10))


def messages(resp):
    return resp.context['messages']._loaded_messages
