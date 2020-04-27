""" Data import """

import os, csv

from dateutil import parser

from ..api.models import *

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

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
            if skip_existing and Image.query.filter_by(Image_Key=row['Image_Key']).count() > 0:
                continue
            print('Importing ...', count, '/', total)
            img = Image(
                Image_Key       = row['Image_Key'],
                Filename        = row['Filename'],
                Canton          = row['Canton'],
                Latitude        = float(row['Latitude']),
                Longitude       = float(row['Longitude']),
                Camera_Angle    = float(row['Camera_Angle']),
                Sequence_Key    = row['Sequence_Key'],
                Captured_At     = parser.parse(row['Captured_At']),
                Panorama        = bool(row['Panorama'])
            )
            db.session.add(img)
            if count % 200 == 0:
                db.session.commit()
