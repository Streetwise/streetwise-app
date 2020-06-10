""" Data import """

import os, csv

from dateutil import parser

from ..models import Image, Campaign
from .. import db

# ../../data/ch_data.csv
DEFAULT_DATA_PATH = os.getenv('DATA_PATH', os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'ch_data.csv')))
DEFAULT_CAMPAIGN = os.getenv('CAMPAIGN', 'safety')

def load_images(skip_existing=True, filename=DEFAULT_DATA_PATH, campaign_name=DEFAULT_CAMPAIGN):
    if not skip_existing:
        print("Warning: skipping existance check, images may be duplicated")

    # Surely there's a better way to count rows in 2020
    with open(filename) as csvfile:
        total = count = 0
        for row in csv.reader(csvfile):
            total = total + 1
        total = total - 1 # skip header
        print(total, 'rows loaded')

    # Set up a campaign
    campaign = Campaign.query.filter_by(name=campaign_name).first()
    if not campaign:
        print("Creating campaign:", campaign_name)
        campaign = Campaign(name=campaign_name)
        db.session.add(campaign)
        db.session.commit()
    campaign_id = campaign.id

    # Main importer
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            count = count + 1
            ik = row['Image_Key']
            img = None
            if skip_existing:
                img = Image.query.filter_by(key=ik).first()
                if img: print('Skipping', ik)
            if not img:
                print('Importing', ik, ' ...', count, '/', total)
                img = Image(
                    campaign        = campaign,
                    key             = ik,
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
                # To improve performance
                if count % 200 == 0:
                    db.session.commit()
        db.session.commit()
