# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from google.appengine.ext import db
from ragendja.auth.models import EmailUserTraits
from ragendja.dbutils import get_object_or_404

class User(EmailUserTraits):
    username = db.StringProperty(required=True, verbose_name=_('username'))
    email = db.EmailProperty(verbose_name=_('e-mail address'))
    name = db.StringProperty(verbose_name=_('name'))
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.name
    
    @classmethod
    def get_user_by_username_or_404(cls, username):
        return get_object_or_404(User, key_name='key_' + username)