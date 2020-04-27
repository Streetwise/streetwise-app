"""
API Models
"""

from datetime import datetime

from .. import Config

IMG_BASE_URL = Config.IMAGE_BUCKET_URL

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Base(db.Model):
    __abstract__  = True
    id            = db.Column(db.Integer, primary_key=True)
    created       = db.Column(db.DateTime,  default=db.func.current_timestamp())
    updated       = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class Image(Base):
    Image_Key = db.Column(db.String(100))
    Filename = db.Column(db.String(100))
    Canton = db.Column(db.String(10))
    Latitude = db.Column(db.Float())
    Longitude = db.Column(db.Float())
    Camera_Angle = db.Column(db.Float())
    Sequence_Key = db.Column(db.String(100))
    Captured_At = db.Column(db.DateTime())
    Panorama = db.Column(db.Boolean())

    @property
    def Url(self):
        return IMG_BASE_URL + self.Filename

    def __repr__(self):
        return self.Image_Key

class Vote(Base):
    # user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    # user = db.relationship(User, description='The user that made the vote')

    choice_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    choice = db.relationship(Image, foreign_keys=[choice_id]) #, description='The image chosen')
    other_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    other = db.relationship(Image, foreign_keys=[other_id]) #, description='The image that was NOT chosen')

    is_leftimage = db.Column(db.Boolean()) #, description='True if the chosen image was on the left')
    is_undecided = db.Column(db.Boolean()) #, description='True if the user was undecided')
    time_elapsed = db.Column(db.Integer) #, description='Seconds elapsed since the image was shown')


class VoteSession(object):
    def __init__(self):
        self.votes = []
        self.counter = 0
        # self.user = 0

    def get(self, id):
        for vote in self.votes:
            if vote['id'] == id:
                return vote
        return None

    def create(self, data):
        vote = Vote(
            choice = Image.query.get(int(data['choice_id'])),
            other =  Image.query.get(int(data['other_id'])),
            is_leftimage = bool(data['is_leftimage']),
            is_undecided = bool(data['is_undecided']),
            time_elapsed = int(data['time_elapsed'])
        )
        print(vote.choice.id, vote.other.id)
        self.counter = self.counter + 1
        self.votes.append(vote)
        return vote
