DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'wrong_parking_set',
        'USER': 'wrong_parking_set',
        'PASSWORD': 'wrong_parking_set',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['15.206.114.172','parking2.sudofire.com']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'