class Config(object): # it inherits form object
    # This is a base CONFIG CLASS
    # define global atributes that our config class would have
    DEBUG = False
    TESTING = False

    SECRET_KEY = 'a_IdjYHAT7NB0zNlkVk2Ca2sVpo'
    SECURITY_PASSWORD_SALT = ')89epiOlyqFb7WdQvbsw'

    SESSION_PERMANENT=False

    # we can overwrite this values in our child classes
    # DB_NAME = "nbnp_db"
    # DB_USERNAME = "nbnp2022"
    # DB_PASSWORD = "root"

    MONGODB_SETTINGS = {
    'db': 'nbnp_db',
    'host': 'mongodb+srv://marijanec:neceva97@cluster0.vzwbn.mongodb.net/nbnp_db?retryWrites=true&w=majority'
    }   

    UPLOADS_AUDIO_FILES = "/home/marijan/nbnp/app/static/uploads/audio"# r"\\wsl$\Ubuntu-20.04\home\marijan\nbnp\app\static\uploads\audio"
    # UPLOADS_TXT_FILES = r"\\wsl$\Ubuntu-20.04\home\marijan\nbnp\app\static\uploads\txt"
    ALLOWED_AUDIO_EXTENSIONS = ["MP3", "MP4", "WAV"]

    SESSION_COOKIE_SECURE = True #we will only send cookies back and forth if there is a secure HTTPS conection

    NBNP_MAIL_SUBJECT_PREFIX = '[SpeechAI]'
    NBNP_MAIL_SENDER = 'SpeechAI Admin <speechai@example.com>'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'neceva.work@gmail.com'
    MAIL_PASSWORD = 'marija(997)neceva'


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False #we don't send request over HTTPS


class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False