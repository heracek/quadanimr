# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

from custom_user.models import User

class AnimationType(db.Model):
    version = db.IntegerProperty(required=True)
    photo_height = db.IntegerProperty(required=True)
    photo_width = db.IntegerProperty(required=True)
    frame_height = db.IntegerProperty(required=True)
    frame_width = db.IntegerProperty(required=True)
    json_info = db.TextProperty(required=True)
    type = db.StringProperty(required=True, choices=['photo', 'thumb'])
    thumb_anim = db.SelfReferenceProperty()
    

class PhotoFile(db.Model):
    blob = db.BlobProperty(required=True)
    
    def __unicode__(self):
        return u'PhotoFile: %s' % self.key()
    

class Photo(db.Model):
    file = db.ReferenceProperty(PhotoFile, required=True)
    user = db.ReferenceProperty(User, required=True)
    anim_type = db.ReferenceProperty(AnimationType, required=True)
    anim_frame_time = db.FloatProperty(required=True)
    description = db.TextProperty()
    date_added = db.DateTimeProperty(required=True, auto_now_add=True)
    
    # - denormalized fields -
    anim_version = db.IntegerProperty()
    anim_frame_height = db.IntegerProperty()
    anim_frame_width = db.IntegerProperty()
    anim_json_info = db.TextProperty()
    
    def set_denormalized_fields(self):
        anim = self.anim_type
        
        self.anim_version = anim.version
        self.anim_frame_height = anim.frame_height
        self.anim_frame_width = anim.frame_width
        self.anim_json_info = anim.json_info
    # ~ denormalized fields ~
    
    def file_key(self):
        return self._file
    
    @permalink
    def get_photo_img_url(self):
        return ('quadanimr_app.views.download_photo', (), {'key': self.file_key()})
    

class ThumbnailFile(db.Model):
    blob = db.BlobProperty(required=True)
    
    def __unicode__(self):
        return u'PhotoFile: %s' % self.key()
    

class Thumbnail(db.Model):
    file = db.ReferenceProperty(ThumbnailFile, required=True)
    photo = db.ReferenceProperty(Photo, required=True)
    
    # - denormalized fields -
    photo_user = db.ReferenceProperty(User)
    photo_anim_frame_time = db.FloatProperty()
    photo_date_added = db.DateTimeProperty()
    photo_anim_type_thumb_anim = db.ReferenceProperty(AnimationType)
    photo_anim_type_version = db.IntegerProperty()
    photo_anim_json_info = db.TextProperty()
    
    def set_denormalized_fields(self):
        photo = self.photo
        thumb_anim = photo.anim_type.thumb_anim
        
        self.photo_user = photo.user
        self.photo_anim_frame_time = photo.anim_frame_time
        self.photo_date_added = photo.date_added
        self.photo_anim_type_thumb_anim = thumb_anim
        self.photo_anim_type_version = thumb_anim.version
        self.photo_anim_json_info = thumb_anim.json_info
    # ~ denormalized fields ~
    
    def file_key(self):
        return self._file
    
    def photo_key(self):
        return self._photo
    
    @permalink
    def get_thumb_img_url(self):
        return ('quadanimr_app.views.download_thumb', (), {'key': self.file_key()})
    
