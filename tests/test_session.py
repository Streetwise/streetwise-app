""" Python unit tests """

import pytest, json

from streetwise.models import Campaign
from . import app, app_context, db

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_campaign_all(client):
    with app_context:
        campaign1 = Campaign()
        campaign2 = Campaign()
        db.session.add(campaign1)
        db.session.add(campaign2)
        db.session.commit()

        resp = client.get('/api/campaign/all')
        assert resp.status_code == 200

        result = json.loads(resp.data)
        assert len(result)>1

def test_campaign_sequence(client):
    with app_context:
        resp = client.get('/api/campaign/next')
        result1 = json.loads(resp.data)
        resp = client.get('/api/campaign/next')
        result2 = json.loads(resp.data)
        assert result1['id'] != result2['id']

def test_campaign_post(client):
    with app_context:
        resp = client.post('/api/campaign/next', json={'campaign_id':None})
        result1 = json.loads(resp.data)
        id1 = result1['id']
        resp = client.post('/api/campaign/next', json={'campaign_id':id1})
        result2 = json.loads(resp.data)
        assert result1['id'] != result2['id']
