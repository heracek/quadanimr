# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from models import Photo, Thumbnail
from views import *

urlpatterns = patterns('',
    url(r'^photo/get/thumb/(?P<key>.+)/$', download_thumb),
    url(r'^photo/get/photo/(?P<key>.+)/$', download_photo),
    
    url(r'^photo/generate-anim-types/$', generate_anim_types),
    url(r'^photo/upload/$', upload_photo),
    
    url(r'^$', 'django.views.generic.list_detail.object_list', {
        'queryset': Thumbnail.all().order('-photo_date_added'),
        'template_name': 'homepage.html',
        'extra_context': { 'viewed_username': 'public', },
    }),
    url(r'^public/photo/(?P<key>.+)/$', show_public_photo),
    
    url(r'^(?P<username>[a-z_]+)/$', users_page),
    url(r'^(?P<username>[a-z_]+)/photo/(?P<photo_key>.+)/$', users_photo),
)
