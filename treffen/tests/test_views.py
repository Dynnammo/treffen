from django import urls
import pytest


@pytest.mark.parametrize('param', [(
    'homepage'
)])
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)

    assert resp.status_code == 200
