"""
Service with a smile
http://flask-restplus.readthedocs.io
"""

from datetime import datetime

from flask import request, current_app
from flask_restplus import Resource, fields

from . import db, api_rest, api_limiter
from .security import require_auth
from ..models import Session, Vote, Image, Campaign, generate_hash

from sqlalchemy.sql.expression import func

ns = api_rest.namespace('vote',
    description = 'Vote operations'
)

VotingModel = api_rest.model('Vote', {
    'choice_id': fields.Integer,
    'other_id': fields.Integer,
    'is_leftimage': fields.Boolean,
    'is_undecided': fields.Boolean,
    'time_elapsed': fields.Integer,
    'comment': fields.String,
    'window_width': fields.Integer(attribute='session.agent_width'),
    'window_height': fields.Integer(attribute='session.agent_height'),
    'session_hash': fields.String(attribute='session.hash'),
})

class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]

@ns.route('/export')
class VoteExport(SecureResource):
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
        latest_vote = Vote.query.first()
        if latest_vote is None: return {}
        latest_vote = latest_vote.created
        vote_count = db.session.query(func.count(Vote.id)).scalar()
        return {
            'total_count':  vote_count,
            'latest_vote': latest_vote.isoformat(),
            'elapsed_seconds': int((datetime.now() - latest_vote).seconds)
        }

@ns.route('/')
class VoteCast(Resource):
    """ Collect user votes """

    decorators = [api_limiter.limit('1/second')]

    @ns.doc('create_vote')
    @ns.expect(VotingModel)
    @ns.marshal_with(VotingModel, code=201)
    def post(self):
        '''Create a new vote'''
        data = api_rest.payload
        if not data:
            return 'No data', 500
        session = None
        if 'session_hash' in data and data['session_hash']:
            my_sh = data['session_hash']
            # Sessions have unique hashes
            session = Session.query.filter_by(hash=my_sh).one_or_none()
        if session is None:
            my_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) or request.remote_addr
            my_ua = request.user_agent
            my_campaign = Campaign.query.first() # No support for multiple campaigns yet
            session = Session(
                hash = generate_hash(),
                campaign = my_campaign,
                agent_address = my_ip,
                agent_platform = my_ua.platform,
                agent_browser = my_ua.browser,
                agent_version = my_ua.version,
                agent_string = my_ua.string,
                agent_height = data['window_height'],
                agent_width = data['window_width']
            )
            db.session.add(session)
            db.session.commit()
        new_vote = Vote(
            session = session,
            comment = data['comment'],
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
            return 'Error saving vote', 500
        current_app.logger.info('Vote committed')
        return new_vote, 201


@ns.route('/survey')
class Survey(Resource):
    """ Collect user survey """

    @ns.doc('submit_survey')
    def post(self):
        '''Save results of survey'''
        data = api_rest.payload
        session = None
        if not data:
            return 'No data', 500
        if 'session_hash' in data and data['session_hash']:
            my_sh = data['session_hash']
            session = Session.query.filter_by(hash=my_sh).one_or_none()
        if not session:
            current_app.logger.warn('No session data')
            return 'No session', 500
        # Update the session data
        session.is_complete = True
        session.response = data['survey_data']
        try:
            db.session.add(session)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            current_app.logger.error('Error saving session {}'.format(str(err)))
            return 'Error saving session', 500
        current_app.logger.info('Session committed')
        return 'OK', 201
