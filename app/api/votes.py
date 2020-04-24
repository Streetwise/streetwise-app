"""
Votes Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request
from flask_restplus import Resource, fields

from .security import require_auth
from . import api_rest

vote = api_rest.model('Vote', {
    'id': fields.Integer(readonly=True, description='The vote unique identifier'),
    'timestamp': fields.DateTime(required=True, description='Time stamp of this vote'),
    'choice': fields.String(required=True, description='The image chosen'),
    'other': fields.String(required=True, description='The image NOT chosen'),
    'is_left': fields.Boolean(required=False, description='True if the selected image was on the left'),
    'is_undecided': fields.Boolean(required=False, description='True if the user was undecided'),
    'timetaken': fields.Integer(required=False, description='Seconds elapsed since image was shown')
})

class VoteClass(object):
    def __init__(self):
        self.counter = 0
        self.user_id = 0
        self.votes = []

    def get(self, id):
        for vote in self.votes:
            if vote['id'] == id:
                return vote
        api.abort(404, "Vote {} doesn't exist".format(id))

    def create(self, data):
        vote = data
        vote['timestamp'] = datetime.utcnow().isoformat()
        vote['id'] = self.counter = self.counter + 1
        self.votes.append(vote)
        return vote

    def update(self, id, data):
        vote = self.get(id)
        vote.update(data)
        return vote

    def delete(self, id):
        vote = self.get(id)
        self.votes.remove(todo)

ns = api_rest.namespace('votes', description='Vote operations')

VOTESESSION = VoteClass()

@ns.route('/')
class CastVote(Resource):
    """ Collect user votes """

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
