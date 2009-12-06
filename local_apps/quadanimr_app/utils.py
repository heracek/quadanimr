from google.appengine.api import images
from google.appengine.ext import db

from models import Photo, PhotoFile, Thumbnail, ThumbnailFile, AnimationType

def get_anim_type_for_photo_size(width, height):
    return AnimationType.all().filter('type =', 'photo').\
                               filter('photo_height =', height).\
                               filter('photo_width =', width).\
                               fetch(1)[0]


def create_and_save_new_photo_with_thumb(user, file_content, description=u''):
    img = images.Image(file_content)
    
    anim = get_anim_type_for_photo_size(img.width, img.height)
    thumb_anim = anim.thumb_anim
    
    # img.resize()
    thumb_img = images.resize(file_content, thumb_anim.photo_width, thumb_anim.photo_height)
    # thumb_img = img.execute_transforms(output_encoding=images.JPEG)
    
    # raise Exception(db.Blob(img))
    # raise Exception('%s\n%s' % (dir(img), img.__dict__))
    photo_file = PhotoFile(
        blob=db.Blob(file_content)
    )
    photo_file.put()
    
    photo = Photo(
        file=photo_file,
        user=user,
        anim_type=anim,
        anim_frame_time=0.25,
        description=description
    )
    photo.set_denormalized_fields()
    photo.put()
    
    thumb_file = ThumbnailFile(
        blob=thumb_img
    )
    thumb_file.put()
    
    thumb = Thumbnail(
        file=thumb_file,
        photo=photo
    )
    thumb.set_denormalized_fields()
    thumb.put()
    
    return photo
