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

IMAGE_DISPAY_MAP = {}
IMAGE_RESPONSE_COUNT = 2

ImageModel = api_rest.model('Image', {
    'id': fields.Integer,
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


@ns.route('/random')
class ImageRandom(Resource):
    """ Get two random images """

    @ns.doc('random_images')
    @ns.marshal_list_with(ImageModel)
    def get(self):
        images = Image.query.order_by(func.random()).limit(10).all()
        sortedImages = sortImagesByDisplayCount(images)
        leastDispalyedImages = selectLeastDisplayedImages(sortedImages)
        for i in leastDispalyedImages:
            incrementImageDisplayCount(i)
        return leastDispalyedImages, 201

@ns.route('/<int:image_id>')
class ImageSelect(Resource):
    """ Return a specific images data """

    @ns.doc('get_image')
    @ns.marshal_with(ImageModel, code=201)
    def get(self, image_id):
        return Image.query.get(image_id), 201

def selectLeastDisplayedImages(sortedImageList):
    images = sortedImageList[0:IMAGE_RESPONSE_COUNT]
    return list(map(lambda i: i[0], images))

def sortImagesByDisplayCount(images):
    imageCount = {}
    for i in images:
        if not IMAGE_DISPAY_MAP.get(i.id):
            imageCount[i] = 1
        else:
            imageCount[i] = IMAGE_DISPAY_MAP[i.id]
    return sorted(imageCount.items(), key=lambda n: n[1])

def incrementImageDisplayCount(imageId):
    if not IMAGE_DISPAY_MAP.get(imageId):
        IMAGE_DISPAY_MAP[imageId] = 1
    else:
        IMAGE_DISPAY_MAP[imageId] += 1