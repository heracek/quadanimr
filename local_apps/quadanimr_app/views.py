# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.simplejson import dumps
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_detail
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response

from forms import PhotoForm
from models import Photo, PhotoFile, Thumbnail, ThumbnailFile, AnimationType
from utils import create_and_save_new_photo_with_thumb

def generate_anim_types(request):
    SINGLE_THUMB_ANIMATION_TYPE_TODO_REMOVE = AnimationType(
        version=1,
        photo_width=180,
        photo_height=120,
        frame_width=45,
        frame_height=45,
        json_info=dumps([[0, 8], [45, 8], [90, 8], [135, 8],
                         [0,68], [45,68], [90,68], [135,68]]),
        type='thumb'
    )
    SINGLE_THUMB_ANIMATION_TYPE_TODO_REMOVE.put()

    SINGLE_ANIMATION_TYPE_TODO_REMOVE = AnimationType(
        version=1,
        photo_width=1200,
        photo_height=800,
        frame_width=300,
        frame_height=400,
        json_info=dumps([[0,  0], [300,  0], [600,  0], [900,  0],
                         [0,400], [300,400], [600,400], [900,400]]),
        type='photo',
        thumb_anim=SINGLE_THUMB_ANIMATION_TYPE_TODO_REMOVE
    )
    SINGLE_ANIMATION_TYPE_TODO_REMOVE.put()
    return HttpResponse('generate_anim_types(): ok!')


def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        
        if form.is_valid():
            photo = create_and_save_new_photo_with_thumb(request.user, form.cleaned_data['photo'].file.read(), form.cleaned_data['description'])
            return HttpResponse('photo uploaded')
    else:
        form = PhotoForm()
    
    return render_to_response(request, 'photo/upload.html', {
        'form': form,
    })


def _download_blob(request, key, model_class):
    obj = get_object_or_404(model_class, key)
    return HttpResponse(obj.blob,
        content_type='image/jpeg')


def download_thumb(request, key):
    return _download_blob(request, key, ThumbnailFile)


def download_photo(request, key):
    return _download_blob(request, key, PhotoFile)


def show_photo(request, key):
    return object_detail(request, Photo.all(), key,
        template_name='photo/show.html',
        template_object_name='photo')
