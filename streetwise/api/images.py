"""
Images routing blueprint
http://flask-restplus.readthedocs.io
"""

from flask import request, g
from flask_restplus import Resource, fields
from sqlalchemy.sql.expression import func

from ..models import Image
from . import api_rest

from .helper.image_tracker import (
    init_image_counter, least_displayed_images
)

ns = api_rest.namespace('image',
    description = 'Image operations'
)

# How many images to randomly select before counting
IMAGES_RANDOM_WALK = 50

# Max. number of images to return in 'all'
IMAGES_SHOWN_ALL = 100

ImageModel = api_rest.model('Image', {
    'id': fields.Integer,
    'campaign_id': fields.Integer,
    'skip': fields.Boolean,
    'key': fields.String,
    'filename': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'canton': fields.String,
    'camera_angle': fields.Float,
    'sequence_key': fields.String,
    'is_panorama': fields.Boolean,
    'captured_at': fields.DateTime,
    'Url': fields.String, # TODO: inconsistent capitalisation
})

@ns.route('/all')
class ImageBrowser(Resource):
    """ List images, for testing """

    @ns.doc('list_images')
    @ns.marshal_list_with(ImageModel)
    def get(self):
        return Image.query.limit(IMAGES_SHOWN_ALL).all()

@ns.route('/random/<int:campaign_id>')
class ImageRandom(Resource):
    """ Get two random images from campaign """

    @ns.doc('random_images')
    @ns.marshal_list_with(ImageModel)
    def get(self, campaign_id):
        # Prime the image counter if needed
        if not 'image_counter' in g:
            g.image_counter = init_image_counter()

        # If the cache is empty, collect fresh data
        images = None
        if g.image_counter.queue is None:
            # Select showable images
            images = Image.query.filter_by(campaign_id=campaign_id, shown=True)
            # Retrieve a random selection
            images = images.order_by(func.random()).limit(IMAGES_RANDOM_WALK).all()

        # Obtain the two least tracked images from queue / the selection
        img2, cache = least_displayed_images(2, images, campaign_id, g.image_counter)
        g.image_counter = cache
        return img2, 201

@ns.route('/<int:image_id>')
class ImageSelect(Resource):
    """ Return a specific images data """

    @ns.doc('get_image')
    @ns.marshal_with(ImageModel, code=201)
    def get(self, image_id):
        return Image.query.get(image_id), 201
