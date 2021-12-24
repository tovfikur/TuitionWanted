from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y7h(c*#0ygc82mti9b@%y_9@@-2k28a+6_3yzk75pm)hce01t!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 900  # set just 10 seconds to test
SESSION_SAVE_EVERY_REQUEST = True
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'FollowUp',
    'GuardianArea',
    'Teacher',
    'admin_adv_search_builder',
    'rest_framework',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
]

X_FRAME_OPTIONS = '*'

ROOT_URLCONF = 'TuitionWanted.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TuitionWanted.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]
AUTH_USER_MODEL = 'FollowUp.User'


# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC6'
TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGOUT_REDIRECT_URL = '/api-auth/login/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_UI_TWEAKS = {
    #     "navbar_small_text": False,
    #     "footer_small_text": False,
    "body_small_text": True,
    #     "brand_small_text": False,
    #     "brand_colour": False,
    #     "accent": "accent-primary",
    #     "navbar": "navbar-dark",
    #     "no_navbar_border": False,
    #     "navbar_fixed": False,
    #     "layout_boxed": False,
    #     "footer_fixed": True,
    #     "sidebar_fixed": False,
    #     "sidebar": "sidebar-dark-primary",
    #     "sidebar_nav_small_text": False,
    #     "sidebar_disable_expand": False,
    #     "sidebar_nav_child_indent": False,
    #     "sidebar_nav_compact_style": False,
    #     "sidebar_nav_legacy_style": False,
    #     "sidebar_nav_flat_style": False,
    #     "theme": "default",
    "dark_mode_theme": "darkly",
    #     "button_classes": {
    #         "primary": "btn-primary",
    #         "secondary": "btn-secondary",
    #         "info": "btn-outline-info",
    #         "warning": "btn-outline-warning",
    #         "danger": "btn-outline-danger",
    #         "success": "btn-outline-success"
    #     },
    #     "actions_sticky_top": False
}

JAZZMIN_SETTINGS = {

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # external url that opens in a new window (Permissions can be added)
        {"name": "Call Support", "url": "tel://+8801796693300", "new_window": True},
        {"name": "SMS", "url": "/follow/sms/", "modal": True},
        {"name": "Follow", "url": "/follow/", "modal": True},
        {"name": "Reminders", "url": "/follow/reminders/", "modal": True},
        # model admin to link to (Permissions checked against model)
        {"model": "FollowUp.User"},

    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["GuardianArea.GuardianDetails", "GuardianArea.Child",
                              "GuardianArea.ChildGroup", "GuardianArea.Note", "GuardianArea.Post",
                              "Teacher", "FollowUp",
                              "FollowUp.GuardianHistory", "FollowUp.TeacherHistory",
                              "FollowUp.PermanentTuitionForChild", "FollowUp.AssignedTeacherForChild",
                              "FollowUp.ShortListedTuitionForChild", "FollowUp.TemporaryTuitionForChild",
                              "FollowUp.User", "auth"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "admin.LogEntry": "fas fa-clipboard-list",
        "FollowUp.User": "fas fa-user",
        "auth.Group": "fas fa-users",

        "Teacher.Subject": "fas fa-book",
        "Teacher.Teacher": "fas fa-chalkboard-teacher",
        "Teacher.TeachingSection": "fas fa-puzzle-piece",
        "Teacher.University": "fas fa-university",

        "FollowUp.TemporaryTuitionForChild": "fas fa-balance-scale-right",
        "FollowUp.ShortListedTuitionForChild": "fas fa-balance-scale-left",
        "FollowUp.AssignedTeacherForChild": "fas fa-balance-scale",
        "FollowUp.PermanentTuitionForChild": "fas fa-handshake",
        "FollowUp.TeacherHistory": "fas fa-history",
        "FollowUp.GuardianHistory": "fas fa-history",
        "FollowUp.SMS": "fas fa-comment",
        "FollowUp.EmployeeLoginHistory": "fas fa-hourglass-half",

        "GuardianArea.GuardianDetails": "fas fa-asterisk",
        "GuardianArea.Child": "fas fa-child",
        "GuardianArea.ChildGroup": "fas fa-user-friends",
        "GuardianArea.Note": "fas fa-sticky-note",

    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": True,
    "custom_js": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "collapsible",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs",
                                    "GuardianArea.Child": "carousel"},
}
