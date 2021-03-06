""" Python unit tests """

import pytest, json

from streetwise.models import Image
from . import app, app_context, db

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_vote_count(client):
    resp = client.get('/api/vote/count')
    assert resp.status_code == 200

def test_vote_patch(client):
    resp = client.patch('/api/vote/')
    assert resp.status_code == 405

def test_secure_resource_fail(client):
    resp = client.get('/api/results/latest')
    assert resp.status_code == 401

def test_secure_resource_pass(client):
    resp = client.get('/api/results/latest',
                      headers={'authorization': 'OpenData'})
    assert resp.status_code == 200

def test_post_and_export(client):
    with app_context:
        image1 = Image()
        image2 = Image()
        db.session.add(image1)
        db.session.add(image2)
        db.session.commit()

        campaign_id = 1
        vote_request = {"choice_id": image1.id,
                        "other_id": image2.id,
                        "campaign_id": campaign_id,
                        "is_leftimage": False, "is_undecided": False,
                        "window_width": 647, "window_height": 928,
                        "time_elapsed": 2,
                        "comment": ""}

        resp = client.post('/api/vote/', json=vote_request)
        assert resp.status_code == 201

        resp = client.get('/api/results/latest',
                        headers={'authorization': 'OpenData'})
        assert resp.status_code == 200

        result = json.loads(resp.data)
        assert vote_request['choice_id'] == result[0]['right_image']['id']
        assert result[0]['campaign']['id'] == campaign_id
        assert result[0]['campaign']['name'] == None # default
