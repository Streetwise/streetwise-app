"""
Helper module that maintains the image display count
"""

from sqlalchemy.sql.expression import func
from streetwise.models import Vote, Image

IMAGE_COUNTER_DICT = {}

def image_display_count():
    """
    Returns a list of tuple of the form (image_id, campaign_id, count)
    where `count` represents the number of times an image was shown.

    Since the votes table stores the image_id as choice and other, we have to query the db
    twice to figure out the images that were selected and rejected. (This query also takes
    into account the Image pairs that didn't have a choice selection)
    """
    selected_images = Vote.query\
                          .join(Image, Image.id == Vote.choice_id)\
                          .with_entities(Image.key, Vote.campaign_id, func.count(Vote.id))\
                          .group_by(Vote.campaign_id, Image.key).all()
    rejected_images = Vote.query\
                          .join(Image, Image.id == Vote.choice_id)\
                          .with_entities(Image.key, Vote.campaign_id, func.count(Vote.id))\
                          .group_by(Vote.campaign_id, Image.key).all()

    list(map(lambda i: i, selected_images + rejected_images))
    return selected_images + rejected_images

def initialize_image_display_counter():
    """
    Initialize the image display counter
    """
    image_campaign_counts = image_display_count()
    for (image_id, campaign_id, count) in image_campaign_counts:
        if IMAGE_COUNTER_DICT.get(image_id) is not None \
           and IMAGE_COUNTER_DICT[image_id].get(campaign_id) is not None:
            # both image and campaign present
            IMAGE_COUNTER_DICT[image_id][campaign_id] += count
        elif IMAGE_COUNTER_DICT.get(image_id) is not None:
            # image is present
            IMAGE_COUNTER_DICT[image_id][campaign_id] = count
        else:
            # neither image nor campaign is present
            IMAGE_COUNTER_DICT[image_id] = {campaign_id: count}

def select_least_displayed_images(sorted_image_list):
    """
    Return two images in the form of a list
    """
    IMAGE_RESPONSE_COUNT = 2
    images = sorted_image_list[0:IMAGE_RESPONSE_COUNT]
    return list(map(lambda i: i[0], images))

def sort_images_by_display_count(images, campaign_id):
    """
    Sorting function for images, based on the frequency of their being displayed
    """
    imageCount = {}
    for image in images:
        if IMAGE_COUNTER_DICT.get(image) is not None \
           and IMAGE_COUNTER_DICT[image].get(campaign_id) is not None:
            imageCount[image] = IMAGE_COUNTER_DICT[image]
            IMAGE_COUNTER_DICT[image] += 1
        elif IMAGE_COUNTER_DICT.get(image) is not None:
            imageCount[image] = 1
            IMAGE_COUNTER_DICT[image][campaign_id] = 1
        else:
            imageCount[image] = 1
            IMAGE_COUNTER_DICT[image] = {campaign_id: 1}
    return sorted(imageCount.items(), key=lambda n: n[1])

def least_displayed_images(images, campaign_id):
    sortedImages = sort_images_by_display_count(images, campaign_id)
    selected_images = select_least_displayed_images(sortedImages)
    return selected_images

