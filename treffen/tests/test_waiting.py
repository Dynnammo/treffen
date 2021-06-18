from django import urls
from factories import PlayerFactory
import pytest

pytestmark = pytest.mark.django_db


def test_waiting(client):
    player = PlayerFactory.create()
    client.cookies['player_id'] = player.id
    url = urls.reverse('waiting_page')
    resp = client.get(url)

    assert resp.status_code == 200
    assert player in resp.context_data.values()
