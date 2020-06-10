"""
App Models
"""

from datetime import datetime
from binascii import b2a_hex
from os import urandom
import re

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
    key = db.Column(db.String(100))
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

    @property
    def json(self):
        return {
            'id':  self.id,
            'key': self.key,
            'filename': self.filename,
            'seq': self.sequence_key,
            'lat': self.latitude,
            'lon': self.longitude
        }

    def __repr__(self):
        return self.key

def generate_hash():
    return str(b2a_hex(urandom(16)), 'utf-8')

class Session(Base):
    __tablename__ = "sessions"

    # A hash to identify this session by
    hash = db.Column(db.String(33), unique=True, default=generate_hash())
    # Agent details for this user session
    agent_address = db.Column(db.String(64))
    agent_platform = db.Column(db.String(128))
    agent_browser = db.Column(db.String(128))
    agent_version = db.Column(db.String(64))
    agent_string = db.Column(db.String(1024))
    agent_width = db.Column(db.Integer())
    agent_height = db.Column(db.Integer())
    # Questionnaire response data
    response = db.Column(db.JSON())
    is_complete = db.Column(db.Boolean(), default=False)

    @property
    def is_mobile_agent(self):
        regexp = r"(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-"
        return re.match(
            regexp,
            self.agent_string,
            flags=re.IGNORECASE
        ) is not None

class Vote(Base):
    __tablename__ = "votes"

    # User session that made the vote
    session_id = db.Column(db.Integer, db.ForeignKey(Session.id))
    session = db.relationship(Session)
    # Campaign that this vote is part of
    campaign_id = db.Column(db.Integer, db.ForeignKey(Campaign.id))
    campaign = db.relationship(Campaign)
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
