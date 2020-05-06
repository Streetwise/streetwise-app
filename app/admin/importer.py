""" Data import """

import os, csv

from dateutil import parser

from ..models import *
from .. import db

# ../../data/ch_data.csv
DEFAULT_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'ch_data.csv'))

def load_images(skip_existing=True, filename=DEFAULT_DATA_PATH):

    with open(filename) as csvfile:
        total = count = 0
        for row in csv.reader(csvfile):
            total = total + 1
        print(total, 'rows loaded')

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            count = count + 1
            if skip_existing and Image.query.filter_by(key=row['Image_Key']).count() > 0:
                continue
            print('Importing ...', count, '/', total)
            img = Image(
                key             = row['Image_Key'],
                filename        = row['Filename'],
                latitude        = float(row['Latitude']),
                longitude       = float(row['Longitude']),
                canton          = row['Canton'],
                camera_angle    = float(row['Camera_Angle']),
                sequence_key    = row['Sequence_Key'],
                is_panorama     = bool(row['Panorama']),
                captured_at     = parser.parse(row['Captured_At']),
            )
            db.session.add(img)
            if count % 200 == 0:
                db.session.commit()
