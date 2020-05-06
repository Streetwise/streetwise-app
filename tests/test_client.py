""" Unit tests for the frontend """

import pytest
from streetwise import create_app, db

app = create_app()
app_context = app.app_context()


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_api(client):
    resp = client.get('/')
    assert resp.status_code == 200
