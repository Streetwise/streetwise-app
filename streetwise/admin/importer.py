""" Data import """

import os, csv

from dateutil import parser

from ..models import Image, Campaign
from .. import db

DEFAULT_DATA_PATH = os.getenv('DATA_PATH', None)
DEFAULT_CAMPAIGN = os.getenv('CAMPAIGN', None)

campaigns = {}

def get_campaign(campaign_name):
    """ Set up the campaign, if needed """
    if campaign_name is None:
        print("Error: use the CAMPAIGN environment variable to set a default")
        exit()
    if campaign_name in campaigns:
        return campaigns[campaign_name]
    campaign = Campaign.query.filter_by(name=campaign_name).first()
    if not campaign:
        print("Creating campaign:", campaign_name)
        campaign = Campaign(name=campaign_name)
        db.session.add(campaign)
        db.session.commit()
    campaigns[campaign_name] = campaign.id
    return campaign.id

def load_images(skip_existing=True, filename=DEFAULT_DATA_PATH, campaign_name=DEFAULT_CAMPAIGN):
    if filename is None:
        print("Error: no image source specified using command or DATA_PATH environment")
        exit()
    if not skip_existing:
        print("Warning: skipping existance check, images may be duplicated")

    # Count rows
    with open(filename) as csvfile:
        total = sum(1 for row in csvfile) - 1
        print(total, 'rows loaded')
        if total < 2:
            exit()

    # Main importer
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        Image_Key = 'Image_Key'
        if '\ufeffImage_Key' in reader.fieldnames:
            Image_Key = '\ufeffImage_Key'
        count = 0
        for row in reader:
            count = count + 1
            ik = row[Image_Key]
            if len(ik) < 22:
                print('Invalid image key', row)
                continue
            img = None
            if 'Campaign' in row:
                campaign_id = get_campaign(row['Campaign'])
            else:
                campaign_id = get_campaign(campaign_name)
            if skip_existing:
                img = Image.query.filter_by(key=ik, campaign_id=campaign_id).first()
                if img:
                    if row['Skip'] == 'TRUE':
                        print('Deactivating', ik)
                        img.shown = False
                        db.session.add(img)
                    #print('Skipping', ik)
                    continue
            if not img:
                print('Importing', ik, ' ...', count, '/', total)
                img = Image(
                    key             = ik,
                    campaign_id     = campaign_id,
                    filename        = row['Filename'],
                    latitude        = float(row['Latitude']),
                    longitude       = float(row['Longitude']),
                    canton          = row['Canton'],
                    camera_angle    = float(row['Camera_Angle']),
                    sequence_key    = row['Sequence_Key'],
                    is_panorama     = bool(row['Panorama']),
                    captured_at     = parser.parse(row['Captured_At']),
                    shown           = (row['Skip'] != 'TRUE')
                )
                db.session.add(img)
                # To improve performance
                if count % 200 == 0:
                    db.session.commit()
        # Commit any remaining
        db.session.commit()
