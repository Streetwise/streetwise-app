"""
App Models
"""

from datetime import datetime
from os import urandom
from binascii import b2a_hex

from . import db, Config

IMG_BASE_URL = Config.IMAGE_BUCKET_URL

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

class Campaign(Base):
    __tablename__ = "campaign"

    # A short way to describe this survey campaign
    name = db.Column(db.String(100))


class Image(Base):
    __tablename__ = "images"

    # Campaign that this image belongs to
    campaign_id = db.Column(db.Integer, db.ForeignKey(Campaign.id))
    campaign = db.relationship(Campaign)
    # Data source identifier
    key = db.Column(db.String(100), unique=True)
    # Filename the image refers to
    filename = db.Column(db.String(100))
    # Geographic coordinates of the photo
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    # If known, the Swiss canton the image is from
    canton = db.Column(db.String(10))
    # Additional details about the shot
    camera_angle = db.Column(db.Float())
    sequence_key = db.Column(db.String(100))
    is_panorama = db.Column(db.Boolean())
    # When was this image taken
    captured_at = db.Column(db.DateTime())

    @property
    def Url(self):
        return IMG_BASE_URL + self.filename

    def __repr__(self):
        return self.key

def generate_hash():
    return str(b2a_hex(urandom(16)), 'utf-8')

class Session(Base):
    __tablename__ = "sessions"

    # A hash to identify this session by
    hash = db.Column(db.String(33), unique=True, default=generate_hash())
    # Campaign that this session belongs to
    campaign_id = db.Column(db.Integer, db.ForeignKey(Campaign.id))
    campaign = db.relationship(Campaign)
    # Agent details for this user session
    agent_address = db.Column(db.String(32))
    agent_platform = db.Column(db.String(64))
    agent_browser = db.Column(db.String(64))
    agent_version = db.Column(db.String(64))
    agent_string = db.Column(db.String(1024))
    agent_width = db.Column(db.Integer())
    agent_height = db.Column(db.Integer())
    # Questionnaire response data
    response = db.Column(db.JSON())
    is_complete = db.Column(db.Boolean(), default=False)

class Vote(Base):
    __tablename__ = "votes"

    # User session that made the vote
    session_id = db.Column(db.Integer, db.ForeignKey(Session.id))
    session = db.relationship(Session)
    # The image chosen
    choice_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    choice = db.relationship(Image, foreign_keys=[choice_id])
    # The image NOT chosen
    other_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    other = db.relationship(Image, foreign_keys=[other_id])
    # True if the chosen image was on the left
    is_leftimage = db.Column(db.Boolean())
    # True if the user was undecided
    is_undecided = db.Column(db.Boolean())
    # Seconds elapsed since the image was shown
    time_elapsed = db.Column(db.Integer)
    # A free text comment, e.g. for undecideds
    comment = db.Column(db.Text)
