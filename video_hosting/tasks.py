import logging

from rest_api_video import app
from video_hosting.models import HashTag


@app.task
def remove_hash_tag_duplicate():
    hashtags_all = HashTag.objects.all()
    for current_tag in hashtags_all:
        current_duplicates = HashTag.objects.filter(tag=current_tag.tag)
        current_duplicates_count = current_duplicates.count()

        if current_duplicates_count >= 2:
            for duplicate in current_duplicates:
                if current_duplicates_count > 1:
                    current_duplicates_count -= 1
                    id_to_delete = duplicate.id
                    duplicate.delete()
                    logging.error(f"duplicate deleted {id_to_delete}")