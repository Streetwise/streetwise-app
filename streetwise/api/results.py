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

class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@ns.route('/export')
class VoteExport(SecureResource):
    """ List all votes entered """

    def voteDict(self):
        id_right = self.other_id if self.is_leftimage else self.choice_id
        id_left = self.other_id if not self.is_leftimage else self.choice_id
        if self.is_undecided:
            the_winner = 'equal'
        elif self.is_leftimage:
            the_winner = 'left'
        else:
            the_winner = 'right'
        return {
            'id': self.id,
            'session_id': self.session.id,
            'created': self.created.isoformat(),
            'left_image_id': id_left,
            'right_image_id': id_right,
            'winner': the_winner,
            'is_undecided': self.is_undecided,
            'time_elapsed': self.time_elapsed,
            'comment': self.comment
        }

    @ns.doc('export_votes')
    def get(self):
        return [voteDict(p) for p in Vote.query
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
