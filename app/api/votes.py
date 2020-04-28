"""
Votes routing blueprint
http://flask-restplus.readthedocs.io
"""

from flask import request, current_app

from flask_restplus import Resource, fields

from .models import VoteSession, Vote, Image
from .security import require_auth

from . import api_rest, api_limiter
from datetime import datetime

from sqlalchemy.sql.expression import func
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

ns = api_rest.namespace('votes',
    description = 'Vote operations'
)

VOTESESSION = VoteSession()

VoteModel = api_rest.model('Vote', {
    'id': fields.Integer,
    'created': fields.DateTime,
    'choice_id': fields.Integer,
    'other_id': fields.Integer,
    'is_leftimage': fields.Boolean,
    'is_undecided': fields.Boolean,
    'time_elapsed': fields.Integer
})


@ns.route('/export')
class ExportVotes(Resource):
    """ List all votes entered """

    @ns.doc('export_votes')
    def get(self):
        return [p.dict() for p in Vote.query
                # .filter_by(is_undecided=False)
                # .limit(24000)
                .all()]

@ns.route('/count')
class VoteCounter(Resource):
    """ Statistics of the votes """

    @ns.doc('count_votes')
    def get(self):
        latest_vote = Vote.query.first().created
        vote_count = db.session.query(func.count(Vote.id)).scalar()
        return {
            'total_count':  vote_count,
            'latest_vote': latest_vote.isoformat(),
            'elapsed_seconds': int((datetime.now() - latest_vote).seconds)
        }

@ns.route('/')
class CastVote(Resource):
    """ Collect user votes """

    decorators = [api_limiter.limit('1/second')]

    # @ns.doc('list_votes')
    # @ns.marshal_list_with(VoteModel)
    # def get(self):
    #     '''List all votes in session'''
    #     return VOTESESSION.votes

    @ns.doc('create_vote')
    @ns.expect(VoteModel)
    @ns.marshal_with(VoteModel, code=201)
    def post(self):
        '''Create a new vote'''
        # vote = VOTESESSION.create(api_rest.payload)
        data = api_rest.payload
        new_vote = Vote(
            choice_id = int(data['choice_id']),
            other_id =  int(data['other_id']),
            is_leftimage = bool(data['is_leftimage']),
            is_undecided = bool(data['is_undecided']),
            time_elapsed = int(data['time_elapsed'])
        )
        try:
            db.session.add(new_vote)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            current_app.logger.error('Error saving vote {}'.format(str(err)))
        current_app.logger.info('Vote committed')
        return new_vote, 201
