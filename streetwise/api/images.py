"""
Images routing blueprint
http://flask-restplus.readthedocs.io
"""

from flask import request
from flask_restplus import Resource, fields
from sqlalchemy.sql.expression import func

from ..models import Image
from . import api_rest

ns = api_rest.namespace('image',
    description = 'Image operations'
)

ImageModel = api_rest.model('Image', {
    'id': fields.Integer,
    'campaign_id': fields.Integer,
    'key': fields.String,
    'filename': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float,
    'canton': fields.String,
    'camera_angle': fields.Float,
    'sequence_key': fields.String,
    'is_panorama': fields.Boolean,
    'captured_at': fields.DateTime,
    'Url': fields.String,
})

@ns.route('/all')
class ImageBrowser(Resource):
    """ List all images available """

    @ns.doc('list_images')
    @ns.marshal_list_with(ImageModel)
    def get(self):
        return Image.query.limit(100).all()

@ns.route('/random/<int:campaign_id>')
class ImageRandom(Resource):
    """ Get two random images from campaign """

    @ns.doc('random_images')
    @ns.marshal_list_with(ImageModel)
    def get(self, campaign_id):
        q = Image.query.filter_by(campaign_id=campaign_id)
        q = q.order_by(func.random()).limit(2).all()
        return q, 201

@ns.route('/<int:image_id>')
class ImageSelect(Resource):
    """ Return a specific images data """

    @ns.doc('get_image')
    @ns.marshal_with(ImageModel, code=201)
    def get(self, image_id):
        return Image.query.get(image_id), 201
