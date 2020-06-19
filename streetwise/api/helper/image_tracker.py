"""
Helper module that maintains the image display count
"""

from sqlalchemy.sql.expression import func
from streetwise.models import Vote, Image

# Holds the image counter dictionary in memory, of the form:
# { 'image key': { campaign_id: count }}
IMAGE_COUNTER_DICT = {}

class ImageCache:
    """
    Simple object to keep the counter and randomized image queue in app memory
    """
    counter: {}
    queue: None
    def __init__(self, counter, queue):
        self.counter = counter
        self.queue = queue

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
      .with_entities(Image.id, Vote.campaign_id, func.count(Vote.id))\
      .group_by(Vote.campaign_id, Image.id).all()
    rejected_images = Vote.query\
      .join(Image, Image.id == Vote.other_id)\
      .with_entities(Image.id, Vote.campaign_id, func.count(Vote.id))\
      .group_by(Vote.campaign_id, Image.id).all()
    return selected_images + rejected_images

def init_image_counter(cache=None):
    """
    Initialize the image display counter
    """
    global IMAGE_COUNTER_DICT
    if cache is not None: IMAGE_COUNTER_DICT = cache.counter
    # Collect image counts
    image_campaign_counts = count_images_from_votes()
    # ..and map them for the appropriate campaign
    for (image_id, campaign_id, count) in image_campaign_counts:
        if not campaign_id in IMAGE_COUNTER_DICT:
            IMAGE_COUNTER_DICT[campaign_id] = {}
        if IMAGE_COUNTER_DICT[campaign_id].get(image_id) is not None:
            IMAGE_COUNTER_DICT[campaign_id][image_id] += count
        else:
            IMAGE_COUNTER_DICT[campaign_id][image_id] = count
    return ImageCache(IMAGE_COUNTER_DICT, None)

def sort_images_by_display_count(images, campaign_id):
    """
    Sorting function for images, based on the frequency of their being displayed
    """
    global IMAGE_COUNTER_DICT
    if not campaign_id in IMAGE_COUNTER_DICT:
        IMAGE_COUNTER_DICT[campaign_id] = {}
    selected_images = {}
    # Add any missing images from this query
    for image in images:
        if IMAGE_COUNTER_DICT[campaign_id].get(image.id) is None:
            IMAGE_COUNTER_DICT[campaign_id][image.id] = 0
        selected_images[image.id] = IMAGE_COUNTER_DICT[campaign_id][image.id]
    # Return the items sorted by count
    return sorted(selected_images.items(), key=lambda item: item[1])

def select_least_displayed(how_many, sorted_image_list):
    """
    Return two image IDs in the form of a list, and record their being displayed
    """
    imageSorted = sorted_image_list[0 : how_many]
    if len(sorted_image_list) >= how_many*3:
        remaining = sorted_image_list[how_many+1]
    else:
        remaining = None
    print(imageSorted)
    imageIDs = list(map(lambda i: i[0], imageSorted))
    images = list(map(lambda i: Image.query.get(i), imageIDs))
    # Increment the tracker
    for image in images:
        IMAGE_COUNTER_DICT[image.campaign.id][image.id] += 1
    return images, ImageCache(IMAGE_COUNTER_DICT, remaining)

def least_displayed_images(howmany, images, campaign, cache=None):
    """
    Returns a number (howmany) of items (images) in order of increasing count,
    for a particular index (campaign), persisted in a store. The optional cache
    persists data between calls.
    """
    global IMAGE_COUNTER_DICT
    sortedImages = None
    if cache is not None:
        IMAGE_COUNTER_DICT = cache.counter
        sortedImages = cache.queue
    if sortedImages is None:
        if images is None: raise Exception("No images in queue")
        sortedImages = sort_images_by_display_count(images, campaign)
    return select_least_displayed(howmany, sortedImages)
