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

current_campaign = None

@ns.route('/next')
class CampaignNext(Resource):
    """ Get alternating campaigns """

    @ns.doc('next_campaign')
    @ns.marshal_list_with(CampaignModel)
    def get(self):
        global current_campaign
        if current_campaign is not None:
            campaign = Campaign.query.get(current_campaign + 1)
        if current_campaign is None or campaign is None:
            campaign = Campaign.query.first()
        current_campaign = campaign.id
        return campaign, 201
