"""
Service with a smile
http://flask-restplus.readthedocs.io
"""

from flask_restplus import Resource
from flask import Response
import json
from sqlalchemy.orm import joinedload

from . import db, api_rest
from .util import require_auth
from ..models import Session, Vote, Image, Campaign

ns = api_rest.namespace('results',
    description = 'Data exports'
)

def voteModel(vote):
    img_right = vote.other if vote.is_leftimage else vote.choice
    img_left = vote.other if not vote.is_leftimage else vote.choice
    if vote.is_undecided:
        the_winner = 'equal'
    elif vote.is_leftimage:
        the_winner = 'left'
    else:
        the_winner = 'right'
    aspect_ratio = round(
        float(vote.session.agent_width) /
        float(vote.session.agent_height), 1)
    aspect_resolution = vote.session.agent_height if aspect_ratio < 1 else vote.session.agent_width
    campaign_id = None if vote.campaign is None else vote.campaign.id
    campaign_name = None if vote.campaign is None else vote.campaign.name

    return {
        'id':              vote.id,
        'created':         vote.created.isoformat(),
        'time_elapsed':    vote.time_elapsed,
        'campaign':        {
            'id':          campaign_id,
            'name':        campaign_name,
        },
        'session': {
            'id':          vote.session.id,
            'is_mobile':   vote.session.is_mobile_agent,
            'is_portrait': aspect_ratio < 1,
            'resolution':  aspect_resolution
        },
        'left_image':      img_left.json,
        'right_image':     img_right.json,
        'winner':          the_winner,
        'comment':         vote.comment
    }

def voteGenerator(votes):
    yield '['
    for vote in votes:
        if vote == votes[-1]:
            yield json.dumps(voteModel(vote))
        else:
            yield json.dumps(voteModel(vote)) + ','
    yield ']'

class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@ns.route('/latest')
class VoteLatest(SecureResource):
    """ List latest votes entered """

    @ns.doc('latest_votes')
    def get(self):
        votes = Vote.query\
                    .enable_eagerloads(True)\
                    .options(joinedload(Vote.other),
                             joinedload(Vote.choice),
                             joinedload(Vote.session),
                             joinedload(Vote.campaign))\
                    .filter_by(is_undecided=False)\
                    .order_by(Vote.created.desc())\
                    .limit(50)\
                    .all()

        return Response(voteGenerator(votes))

@ns.route('/undecided')
class VoteUndecided(SecureResource):
    """ List latest undecided entries """

    @ns.doc('latest_undecided')
    def get(self):
        votes = Vote.query\
                    .enable_eagerloads(True)\
                    .options(joinedload(Vote.other),
                             joinedload(Vote.choice),
                             joinedload(Vote.session),
                             joinedload(Vote.campaign))\
                    .filter_by(is_undecided=True)\
                    .limit(50)\
                    .all()

        return Response(voteGenerator(votes))

@ns.route('/all')
class VoteAll(SecureResource):
    """ List all votes """

    # TODO: consider using CSV for brevity
    @ns.doc('all_votes')
    def get(self):
        votes = Vote.query\
                    .enable_eagerloads(True)\
                    .options(joinedload(Vote.other),
                             joinedload(Vote.choice),
                             joinedload(Vote.session),
                             joinedload(Vote.campaign))\
                    .all()

        return Response(voteGenerator(votes))

