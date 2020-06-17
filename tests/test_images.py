""" Unit tests for the frontend """

import pytest, json

from streetwise.models import Image, Campaign, Vote
from streetwise.api.helper import image_tracker
from . import app, app_context, db

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_image_counter(client):
    with app_context:
        # Create some images and vote on them
        campaign1 = Campaign()
        db.session.add(campaign1)
        images = [
            Image(campaign=campaign1, key=str(i))
            for i in range(0,5)
        ]
        [ db.session.add(img) for img in images ]
        vote1 = Vote(
            campaign=campaign1,
            choice=images[1], other=images[2]
        )
        db.session.add(vote1)
        vote2 = Vote(
            campaign=campaign1,
            choice=images[3], other=images[4]
        )
        db.session.add(vote2)
        db.session.commit()

        image_tracker.init_image_counter()
        # print(image_tracker.IMAGE_COUNTER_DICT)

        resp = client.get('/api/image/random/%d' % campaign1.id)
        assert resp.status_code == 201

        result = json.loads(resp.data)
        assert images[0].id in (result[0]['id'], result[1]['id'])
