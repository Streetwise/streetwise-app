import os
from app import app, admin
from app.api.models import *

with app.app_context():
    db.create_all()
    admin.load_images()
