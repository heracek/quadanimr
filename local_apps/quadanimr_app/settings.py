from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'quadanimr_app/lib/jquery.timers-1.2.js',
    'quadanimr_app/quadanimr.js',
)

settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'quadanimr_app/css/master.css',
    'quadanimr_app/css/screen.css',
)
