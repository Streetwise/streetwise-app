"""
Helper module that maintains the image display count
"""

from sqlalchemy.sql.expression import func
from streetwise.models import Vote, Image

# Holds the image counter dictionary in memory, of the form:
# { 'image key': { campaign_id: count }}
IMAGE_COUNTER_DICT = {}

def count_images_from_votes():
    """
    Returns a list of tuple of the form (image_id, campaign_id, count)
    where `count` represents the number of times an image was shown.
    """
    # Since the votes table stores the image_id as choice and other, we have to query the db
    # twice to figure out the images that were selected and rejected. (This query also takes
    # into account the Image pairs that didn't have a choice selection)
    selected_images = Vote.query\
                          .join(Image, Image.id == Vote.choice_id)\
                          .with_entities(Image.key, Vote.campaign_id, func.count(Vote.id))\
                          .group_by(Vote.campaign_id, Image.key).all()
    rejected_images = Vote.query\
                          .join(Image, Image.id == Vote.other_id)\
                          .with_entities(Image.key, Vote.campaign_id, func.count(Vote.id))\
                          .group_by(Vote.campaign_id, Image.key).all()
    #list(map(lambda i: i, selected_images + rejected_images)) # unused
    return selected_images + rejected_images

def initialize_image_display_counter():
    """
    Initialize the image display counter
    """
    image_campaign_counts = count_images_from_votes()
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

def sort_images_by_display_count(images, campaign_id):
    """
    Sorting function for images, based on the frequency of their being displayed
    """
    for image in images:
        if IMAGE_COUNTER_DICT.get(image.key) is not None \
           and IMAGE_COUNTER_DICT[image.key].get(campaign_id) is not None:
            IMAGE_COUNTER_DICT[image.key][campaign_id] += 1
        elif IMAGE_COUNTER_DICT.get(image.key) is not None:
            IMAGE_COUNTER_DICT[image.key][campaign_id] = 1
        else:
            IMAGE_COUNTER_DICT[image.key] = {campaign_id: 1}
    return sorted(IMAGE_COUNTER_DICT.items())

def select_least_displayed(how_many, sorted_image_list):
    """
    Return two image IDs in the form of a list
    """
    imageSorted = sorted_image_list[0:how_many]
    imageIDs = list(map(lambda i: i[0], imageSorted))
    return list(map(lambda i: Image.query.get(i), imageIDs))

def least_displayed_images(howmany, images, campaign_id):
    """
    Returns a number (howmany) of items (images) in order of increasing count,
    for a particular index (campaign_id)
    """
    sortedImages = sort_images_by_display_count(images, campaign_id)
    selectedImages = select_least_displayed(howmany, sortedImages)
    print(selectedImages)
    return selectedImages
