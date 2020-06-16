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

# In-memory store for image counting at runtime
IMAGE_COUNTER_MAP = {}

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
        return Image.query.limit(100).all()

@ns.route('/random/<int:campaign_id>')
class ImageRandom(Resource):
    """ Get two random images from campaign """

    @ns.doc('random_images')
    @ns.marshal_list_with(ImageModel)
    def get(self, campaign_id):
        images = Image.query.filter_by(campaign_id=campaign_id).order_by(func.random()).limit(10).all()
        sortedImages = sortImagesByDisplayCount(images)
        return selectLeastDisplayedImages(sortedImages), 201

@ns.route('/<int:image_id>')
class ImageSelect(Resource):
    """ Return a specific images data """

    @ns.doc('get_image')
    @ns.marshal_with(ImageModel, code=201)
    def get(self, image_id):
        return Image.query.get(image_id), 201

def selectLeastDisplayedImages(sortedImageList):
    """ Return two images in the form of a list """
    IMAGE_RESPONSE_COUNT = 2
    images = sortedImageList[0:IMAGE_RESPONSE_COUNT]
    return list(map(lambda i: i[0], images))

def sortImagesByDisplayCount(images):
    """ Sorting function for images, based on the frequency of their being displayed """
    imageCount = {}
    for i in images:
        if not IMAGE_COUNTER_MAP.get(i.id):
            imageCount[i] = 1
            IMAGE_COUNTER_MAP[imageId] = 1
        else:
            imageCount[i] = IMAGE_COUNTER_MAP[i.id]
            IMAGE_COUNTER_MAP[imageId] += 1
    return sorted(imageCount.items(), key=lambda n: n[1])
