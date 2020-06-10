"""
Campaigns routing blueprint
http://flask-restplus.readthedocs.io
"""

from flask import request
from flask_restplus import Resource, fields
from sqlalchemy.sql.expression import func

from ..models import Campaign
from . import api_rest

ns = api_rest.namespace('campaign',
    description = 'Campaign operations'
)

CampaignModel = api_rest.model('Campaign', {
    'id': fields.Integer,
    'name': fields.String,
})

@ns.route('/all')
class CampaignBrowser(Resource):
    """ List all current campaigns """

    @ns.doc('list_campaigns')
    @ns.marshal_list_with(CampaignModel)
    def get(self):
        return Campaign.query.all()

@ns.route('/random')
class CampaignRandom(Resource):
    """ Get a random campaign """

    @ns.doc('random_campaign')
    @ns.marshal_list_with(CampaignModel)
    def get(self):
        return Campaign.query.order_by(func.random()).limit(1).all(), 201
