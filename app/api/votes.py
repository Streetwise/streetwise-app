"""
Votes Routing
http://flask-restplus.readthedocs.io
"""

from flask import request

from flask_restplus import Resource, fields

from .models import VoteClass
from .security import require_auth

from . import api_rest, api_limiter

ns = api_rest.namespace('votes',
    description = 'Vote operations'
)

VOTESESSION = VoteClass()

vote = api_rest.model('Vote', {
    'id': fields.Integer(readonly=True, description='The vote unique identifier'),
    'timestamp': fields.DateTime(required=True, description='Time stamp of this vote'),
    'choice': fields.String(required=True, description='The image chosen'),
    'other': fields.String(required=True, description='The image NOT chosen'),
    'is_left': fields.Boolean(required=False, description='True if the selected image was on the left'),
    'is_undecided': fields.Boolean(required=False, description='True if the user was undecided'),
    'timetaken': fields.Integer(required=False, description='Seconds elapsed since image was shown')
})


@ns.route('/')
class CastVote(Resource):
    """ Collect user votes """

    decorators = [api_limiter.limit('1/second')]

    @ns.doc('list_votes')
    @ns.marshal_list_with(vote)
    def get(self):
        '''List all votes'''
        return VOTESESSION.votes

    @ns.doc('create_vote')
    @ns.expect(vote)
    @ns.marshal_with(vote, code=201)
    def post(self):
        '''Create a new vote'''
        return VOTESESSION.create(api_rest.payload), 201
