"""
Campaigns routing blueprint
http://flask-restplus.readthedocs.io
"""

from flask import current_app
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

def getCampaign(campaign_id):
    campaign = None
    query = Campaign.query.order_by(Campaign.id.asc())
    # Select the next campaign in sequence if one is provided
    if campaign_id is not None:
        if isinstance(campaign_id, str) and campaign_id.isdigit():
            campaign_id = int(campaign_id)
            campaign = query.filter(Campaign.id > campaign_id).first()
        if isinstance(campaign_id, int):
            campaign = query.filter(Campaign.id > campaign_id).first()
    # Otherwise take the first campaign in the list
    if campaign_id is None or campaign is None:
        campaign = query.first()
    # Error condition
    if campaign is None:
        current_app.logger.error('No campaigns available')
        return None
    return campaign

@ns.route('/next')
class CampaignNext(Resource):
    """ Get alternating campaigns """

    @ns.doc('next_campaign')
    @ns.marshal_list_with(CampaignModel)
    def get(self):
        global current_campaign
        campaign = getCampaign(current_campaign)
        current_campaign = campaign.id
        return campaign, 201

    @ns.doc('next_campaign_post')
    @ns.marshal_list_with(CampaignModel)
    def post(self):
        ''' Get next campaign from one provided '''
        global current_campaign
        data = api_rest.payload
        if data and 'campaign_id' in data:
            current_campaign = data['campaign_id']
        campaign = getCampaign(current_campaign)
        current_campaign = campaign.id
        return campaign, 201
