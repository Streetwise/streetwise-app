""" Python unit tests """

import pytest

from streetwise.models import Image
from . import app, app_context, db

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_api(client):
    resp = client.get('/api/')
    assert resp.status_code == 200

def test_vote_count(client):
    resp = client.get('/api/vote/count')
    assert resp.status_code == 200

def test_vote_post(client):
    with app_context:
        image1 = Image()
        image2 = Image()
        db.session.add(image1)
        db.session.add(image2)
        db.session.commit()

        vote_request = {"choice_id": image1.id, "other_id": image2.id,
                        "is_leftimage": False,
                        "is_undecided": False, "time_elapsed": 2,
                        "window_width": 647, "window_height": 928,
                        "comment": ""}

        resp = client.post('/api/vote/', json=vote_request)
        assert resp.status_code == 201

def test_vote_patch(client):
    resp = client.patch('/api/vote/')
    assert resp.status_code == 405

def test_secure_resource_fail(client):
    resp = client.get('/api/vote/export')
    assert resp.status_code == 401

def test_secure_resource_pass(client):
    resp = client.get('/api/vote/export',
                      headers={'authorization': 'OpenData'})
    assert resp.status_code == 200

@pytest.fixture(scope="module")
def request_context():
    return app.test_request_context('')

def test_session(request_context):
    with request_context:
        # Do something that requires request context
        assert True
