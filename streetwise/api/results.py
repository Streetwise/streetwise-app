"""
Service with a smile
http://flask-restplus.readthedocs.io
"""

from flask_restplus import Resource

from . import db, api_rest
from .security import require_auth
from ..models import Session, Vote, Image, Campaign

ns = api_rest.namespace('result',
    description = 'Data exports'
)

class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@ns.route('/votes')
class VoteExport(SecureResource):
    """ List all votes entered """

    def voteDict(self, vote):
        id_right = vote.other_id if vote.is_leftimage else vote.choice_id
        id_left = vote.other_id if not vote.is_leftimage else vote.choice_id
        if vote.is_undecided:
            the_winner = 'equal'
        elif vote.is_leftimage:
            the_winner = 'left'
        else:
            the_winner = 'right'
        return {
            'id': vote.id,
            'session_id': vote.session.id,
            'created': vote.created.isoformat(),
            'left_image_id': id_left,
            'right_image_id': id_right,
            'winner': the_winner,
            'is_undecided': vote.is_undecided,
            'time_elapsed': vote.time_elapsed,
            'comment': vote.comment
        }

    @ns.doc('export_votes')
    def get(self):
        return [self.voteDict(p) for p in Vote.query
                # .filter_by(is_undecided=False)
                # .limit(24000)
                .all()]

    # Left image name
    # Coordinates of left image
    # Mapillary Sequence ID / Mapillary image ID for left image
    # Right image name
    # Coordinates of right image
    # Mapillary sequence ID / Mapillary image ID for right image
    # Winner (left, right, undecided)
    # Demographics of the session
    # Mobile / desktop
    # Screen ratio
