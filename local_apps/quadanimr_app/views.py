# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.simplejson import dumps
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_detail, object_list
from ragendja.dbutils import get_object_or_404
from ragendja.template import render_to_response

from custom_user.models import User

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


def show_public_photo(request, key):
    extra_context = {
        'object_list': Thumbnail.all().order('-photo_date_added'),
        'viewed_username': 'public',
    }
    return object_detail(request, Photo.all(), key,
        template_name='photo/public-show.html',
        template_object_name='photo',
        extra_context=extra_context)

def users_photo(request, username, photo_key):
    viewed_user = User.get_user_by_username_or_404(username)
    photo = get_object_or_404(Photo, photo_key)
    
    if photo.user != viewed_user:
        raise Http404('Object does not exist!')
    
    extra_context = {
        'viewed_user': viewed_user,
        'photo': photo,
        'viewed_username': username
    }
    
    return object_list(request,
        queryset=Thumbnail.all().filter('photo_user', viewed_user).order('-photo_date_added'),
        template_name='photo/show.html',
        extra_context=extra_context
    )

def users_page(request, username):
    viewed_user = User.get_user_by_username_or_404(username)
    
    photo = None
    fetched_photo_list = Photo.all().filter('user', viewed_user).order('-date_added').fetch(1)
    if fetched_photo_list:
        photo = fetched_photo_list[0]
    
    extra_context = {
        'viewed_user': viewed_user,
        'photo': photo,
        'viewed_username': username
    }
    
    return object_list(request,
        queryset=Thumbnail.all().filter('photo_user', viewed_user).order('-photo_date_added'),
        template_name='photo/show.html',
        extra_context=extra_context
    )