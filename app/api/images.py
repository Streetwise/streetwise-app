"""
Images routing blueprint
http://flask-restplus.readthedocs.io
"""

from flask import request
from flask_restplus import Resource, fields
from sqlalchemy.sql.expression import func

from .models import Image
from . import api_rest

ns = api_rest.namespace('image',
    description = 'Image operations'
)

ImageModel = api_rest.model('Image', {
    'id': fields.Integer,
    'Url': fields.String,
    'Image_Key': fields.String,
    'Filename': fields.String,
    'Canton': fields.String,
    'Latitude': fields.Float,
    'Longitude': fields.Float,
    'Camera_Angle': fields.Float,
    'Sequence_Key': fields.String,
    'Captured_At': fields.DateTime,
    'Panorama': fields.Boolean
})

@ns.route('/all')
class ImageBrowser(Resource):
    """ List all images available """

    @ns.doc('list_images')
    @ns.marshal_list_with(ImageModel)
    def get(self):
        return Image.query.limit(100).all()


@ns.route('/random')
class ImageRandom(Resource):
    """ Get two random images """

    @ns.doc('random_images')
    @ns.marshal_list_with(ImageModel)
    def get(self):
        return Image.query.order_by(func.random()).limit(2).all(), 201

@ns.route('/<int:image_id>')
class ImageSelect(Resource):
    """ Return a specific images data """

    @ns.doc('get_image')
    @ns.marshal_with(ImageModel, code=201)
    def get(self, image_id):
        return Image.query.get(image_id), 201
