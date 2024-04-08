from decouple import config

class Config():
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

configure = {
    'development': DevelopmentConfig
}


DATABASES = {
    config('ENVIRONMENTS'): {
        'DB_HOST': config('DB_HOST'),
        'DB_USER': config('DB_USER'),
        'DB_PASSWORD': config('DB_PASSWORD'),
        'DB_PORT': config('DB_PORT'),
        'DB_NAME': config('DB_NAME'),
        'DB_TYPE': config('DB_TYPE'),
    },

}