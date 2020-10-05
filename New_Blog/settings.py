"""
Django settings for New_Blog project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'Your key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['47.96.13.183', 'Cuber_CID.com']

# 静态文件收集目录
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
# Application definition
INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps',
    'apps.article',
    'ckeditor',  # 注册富文本编辑器
    'mdeditor',  # 注册支持markdown的富文本编辑器
    'ckeditor_uploader',  # 注册编辑器的文件上传功能
    'apps.userprofile',
    'password_reset',  # 注册密码重置的第三方应用
    'apps.comment',  # 注册评论应用
    'django_tctip',
    'mptt',  # 注册多级评论应用
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'New_Blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'New_Blog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

X_FRAME_OPTIONS = 'SAMEORIGIN'  # Django 3 修改了 xframe 的默认设置，即不支持 iframe 自己,因此通过此设定可以实现支持iframe
# 这句话不能少，否则无法实现将上传的图片显示到前端

# 放在django项目根目录，同时也需要创建media文件夹
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

MEDIA_URL = '/media/'

CKEDITOR_UPLOAD_PATH = 'upload/'

CKEDITOR_CONFIGS = {
    # django-ckeditor默认使用default配置
    # 'default': {
    #     # 编辑器宽度自适应
    #     'width': 'auto',
    #     'height': '200px',
    #     # tab键转换空格数
    #     'tabSpaces': 4,
    #     'toolbar': 'Custom',
    #     # 工具栏按钮
    #
    #     'toolbar_Custom': [
    #         # 表情 代码块
    #         ['Smiley', 'CodeSnippet'],
    #         # 字体风格
    #         ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
    #         # 字体颜色
    #         ['TextColor', 'BGColor'],
    #
    #         ['Form', 'Checkbox', 'Radio', 'Select', 'Button', 'ImageButton', ],
    #         # ['Form', 'Checkbox', 'Radio',  'Select', 'Button', 'ImageButton',]
    #
    #         # 图片，动画
    #         ['Image', 'Table', 'HorizontalRule', 'SpecialChar', ],  # 'PageBreak', 'Iframe'
    #         ['Styles', 'Format', 'Font', 'FontSize'],
    #         # 链接
    #         ['Link', 'Unlink'],
    #         # 列表
    #         ['NumberedList', 'BulletedList'],
    #         # 最大化
    #         ['Maximize']
    #
    #     ],
    #     # 加入代码块插件
    #     'extraPlugins': ','.join(['codesnippet', 'uploadimage', 'widget', 'lineutils', 'prism']),
    # }

    # django-ckeditor默认使用default配置
    'default': {
        # 编辑器宽度自适应
        'width': 'auto',
        'height': '250px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 工具栏按钮
        'toolbar_Custom': [
            # 表情 代码块
            ['Smiley', 'CodeSnippet'],
            # 字体风格
            ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Blockquote'],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 链接
            ['Link', 'Unlink'],
            # 列表
            ['NumberedList', 'BulletedList'],
            # 最大化
            ['Maximize']
        ],
        # 加入代码块插件
        'extraPlugins': ','.join(['codesnippet', 'prism', 'widget', 'lineutils']),
    }
}

MDEDITOR_CONFIGS = {
    'default': {
        'width': '90% ',  # Custom edit box width
        'height': 500,  # Custom edit box height
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime"
                                                                                                           "emoji",
                    "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # image upload format type
        'image_folder': 'editor',  # image save the folder name
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': True,  # whether to open the expression function
        'tex': True,  # whether to open the tex chart function
        'flow_chart': True,  # whether to open the flow chart function
        'sequence': True,  # Whether to open the sequence diagram function
        'watch': True,  # Live preview
        'lineWrapping': False,  # lineWrapping
        'lineNumbers': False,  # lineNumbers
        'language': 'zh'  # zh / en / es
    }

}

# ---------------------------

EMAIL_HOST = 'host email'

EMAIL_HOST_USER = 'your email'

EMAIL_HOST_PASSWORD = 'your host password'

EMAIL_PORT = 0

EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'your default email'

