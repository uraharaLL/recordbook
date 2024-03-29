# -*- coding: UTF-8 -*-
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Komkov Alexander', 'sashakomkov@gmail.com'),
)

MANAGERS = ADMINS

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__));

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'recordbook',
        'USER': 'root',
        'PASSWORD': '123',
    }
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MEDIA_ROOT = os.path.join(PROJECT_DIR, "..", "static")

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

#Количество объектов на странице с пагинатором
PAGINATOR_OBJECTS = 50

USE_I18N = True

USE_L10 = True

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/admin-media/'

SECRET_KEY = '_dyte-9u%m06vwhoyc7ug0n&4olty8*yx+sei8p_zet+)!v8wg'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
                               "django.core.context_processors.auth",
                               "django.core.context_processors.media",
                               'src.context_processors.plural',
                               'src.context_processors.menu',
                               'src.context_processors.environment',
                               'django.contrib.messages.context_processors.messages',
                               )


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'src.userextended.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'src.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, "..", "templates"),
)

#Таймаут для входа/выхода (мин)
TIMEOUT = 20

#Дни недели
WORKDAYS = ( ('1', 'Понедельник'), 
             ('2', 'Вторник'), 
             ('3', 'Среда'), 
             ('4', 'Четверг'), 
             ('5', 'Пятница'), 
             ('6', 'Суббота')
             )

#Номера уроков
LESSON_NUMBERS = ( ('1', '1'), 
                   ('2', '2'), 
                   ('3', '3'),
                   ('4', '4'),
                   ('5', '5'),
                   ('6', '6'),
                   ('7', '7'),
                   ('8', '8'),
                   ('9', '9'),
                   ('10', '10') )

ROOT_CAN_ALL = False

APPEND_SLASH = True

REST_MODELS = ['school', 'grade', 'teacher', 'pupil', 'subject', 'lesson', 'mark', 'resultdate', 'result']
REST_MODELS2APPS = {'school':      ['src.userextended.models.School', 'forms.SchoolRestForm'],
                    'grade':       ['src.userextended.models.Grade', 'forms.GradeRestForm'],
                    'teacher':     ['src.userextended.models.Teacher', 'forms.TeacherRestForm'],
                    'pupil':       ['src.userextended.models.Pupil', 'forms.PupilRestForm'],
                    'subject':     ['src.userextended.models.Subject', 'forms.SubjectRestForm'],
                    'lesson':      ['src.marks.models.Lesson', 'forms.LessonRestForm'],
                    'mark':        ['src.marks.models.Mark', 'forms.MarkRestForm'],
                    'resultdate':  ['src.marks.models.ResultDate', 'forms.ResultDateRestForm'],
                    'result':      ['src.marks.models.Result', 'forms.ResultRestForm'],
                    }


# Настройки для интеграции системы электронных дневников с Google App's (http://www.google.com/apps/intl/ru/group/index.html)
GAPPS_USE = False
GAPPS_LOGIN = 'admin@example.com'
GAPPS_DOMAIN = 'example.com'
GAPPS_PASSWORD = 'password'
MAX_MARK = 5

BASIC_WWW_AUTHENTICATION = True

DATE_FORMAT = "d.m.y"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',

#    'django_extensions',
    
    'pytils',
    'smart_selects',
    'src',
    'src.attendance',
    'src.pages',
    'src.userextended',
    'src.marks',
    'src.curatorship',
    'src.tests',
    'src.rest',
    'src.api',
    'src.billing',
)
