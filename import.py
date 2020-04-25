import os, csv

from dateutil import parser

from app import app, db
from app.api.models import Image

SKIP_EXISTING = False

db.create_all()

with open('data/ch_data.csv') as csvfile:
    total = count = 0
    for row in csv.reader(csvfile):
        total = total + 1
    print(total, 'rows loaded')

with open('data/ch_data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        count = count + 1
        if SKIP_EXISTING and Image.query.filter_by(Image_Key=row['Image_Key']).count() > 0:
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

db.session.close()
