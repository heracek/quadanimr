# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from models import Photo, Thumbnail
from views import *

urlpatterns = patterns('',
    url(r'^photo/generate-anim-types/$', generate_anim_types),
    url(r'^photo/upload/$', upload_photo),
    url(r'^photo/list/$', 'django.views.generic.list_detail.object_list', {
        'queryset': Thumbnail.all().order('-photo_date_added'),
        'template_name': 'photo/list.html',
    }),
    url(r'^photo/show/(?P<key>.+)/$', show_photo),
    url(r'^photo/get/thumb/(?P<key>.+)/$', download_thumb),
    url(r'^photo/get/photo/(?P<key>.+)/$', download_photo),
)
