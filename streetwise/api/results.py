"""
Service with a smile
http://flask-restplus.readthedocs.io
"""

from flask_restplus import Resource

from . import db, api_rest
from .security import require_auth
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
    return {
        'id':              vote.id,
        'created':         vote.created.isoformat(),
        'time_elapsed':    vote.time_elapsed,
        'session': {
            'id':          vote.session.id,
            'campaign':    vote.session.campaign_id,
            'is_mobile':   vote.session.is_mobile_agent,
            'is_portrait': aspect_ratio < 1,
            'resolution':  aspect_resolution
        },
        'left_image':      img_left.json,
        'right_image':     img_right.json,
        'winner':          the_winner,
        'comment':         vote.comment
    }

class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@ns.route('/latest')
class VoteLatest(SecureResource):
    """ List latest votes entered """

    @ns.doc('latest_votes')
    def get(self):
        return [voteModel(p) for p in Vote.query
                .filter_by(is_undecided=False)
                .limit(50)
                .all()]

@ns.route('/undecided')
class VoteUndecided(SecureResource):
    """ List latest undecided entries """

    @ns.doc('latest_undecided')
    def get(self):
        return [voteModel(p) for p in Vote.query
                .filter_by(is_undecided=True)
                .limit(50)
                .all()]

@ns.route('/all')
class VoteAll(SecureResource):
    """ List all votes """

    # TODO: consider using CSV for brevity
    @ns.doc('all_votes')
    def get(self):
        return [voteModel(p) for p in Vote.query.all()]
