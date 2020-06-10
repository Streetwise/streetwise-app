"""
Campaigns routing blueprint
http://flask-restplus.readthedocs.io
"""

from flask import request
from flask_restplus import Resource, fields

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

@ns.route('/next')
class CampaignNext(Resource):
    """ Get the next campaign """

    @ns.doc('next_campaign')
    @ns.marshal_list_with(CampaignModel)
    def get(self):
        # TODO: sequential on user session
        campaign_sequence = 2
        return Campaign.query.get(campaign_sequence), 201
