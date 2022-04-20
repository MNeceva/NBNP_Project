from enum import unique
from xml.dom import ValidationErr
from app import db
from app import app

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app, session
from flask_login import UserMixin

class Users(UserMixin, db.Document):
    firstname = db.StringField(required = True)
    lastname = db.StringField(required = True)
    username = db.StringField(required = True, unique = True)
    # _password = db.StringField(required = True, max_length = 16)
    password_hash = db.StringField(required = True, max_length =128)
    email = db.EmailField(required = True, unique = True)
    gender = db.StringField(required = True)
    birthdate = db.StringField(required = True)
    date_created = db.DateTimeField(default = datetime.utcnow())
    confirmed = db.BooleanField(default = False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(str(self.id), salt=current_app.config['SECURITY_PASSWORD_SALT']) #.decode('utf-8')
        # return s.dumps({'confirm': str(self.id)}, salt=current_app.config['SECURITY_PASSWORD_SALT']) #.decode('utf-8')

    def confirm(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(token,
                        salt=current_app.config['SECURITY_PASSWORD_SALT'],
                        max_age=expiration
                )
        except:
            return False
        if id != str(self.pk):
            return False
        self.confirmed = True
        
        self.save()
        
        return True

        # return id

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(self.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
        # return s.dumps(str(self.pk()), salt=current_app.config['SECURITY_PASSWORD_SALT'])

        # s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        print(new_password)
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'])
        except:
            return False

        print("Pominav reset 1")
       
        try:
            user = Users.objects(email=email).get_or_404()
            print(len(user))
            print(user.firstname)
            user.password=new_password
            # user.update(password=new_password)
            user.save()
            # user.reload()
        except:
            return False

        print("Pominav reset 2")
        
        return True


    meta = {
        'indexes': ['username','email'],
        'ordering': ['-date_created']
    }
    

@login_manager.user_loader
def load_user(user_id):
    # user_id = session.get('id')
    # try:
    #     user=Users.objects(id=user_id).get()
    # except:
    #     return AttributeError("User doesn't exists")
    print(type(user_id))
    # user=Users.objects(id=user_id).get()
    # print(user.email)
    return Users.objects(pk=user_id).first()


class AudioFiles(db.Document):
    name = db.StringField(required = True, unique = True)
    path = db.StringField(required = True)
    format = db.StringField(required = True)
    size = db.IntField(required = True)
    user = db.ReferenceField(Users)
    # audio_file = db.FileField(required = True)
    # txt_file = db.ReferenceField("TxtFiles")
    date_created = db.DateTimeField(default = datetime.utcnow())

    meta = {
        'ordering': ['-date_created']
    }


# class TxtFiles(db.Document):
#     name = db.StringField(required = True)
#     txt_file = db.FileField(required = True)
#     date_created = db.DateTimeField(default = datetime.utcnow())

#     meta = {
#         'ordering': ['-date_created']
#     }

