from settings import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import DateTime, func

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import config


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(128))
    register_date = db.Column(db.DateTime)
    email = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    is_admin = db.Column(db.Boolean)

    def __init__(self, username):
        self.username = username
        self.register_date = datetime.utcnow()
        self.is_admin = False

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def admin(self):
        return self.is_admin

    # default expiration 3600s = 1 hour
    def generate_auth_token(self, expiration=3600 * 7):
        s = Serializer(config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(config.SECRET_KEY)
        try:
            data = s.loads(token)
        # except SignatureExpired:
        #     return None  # valid token, but expired
        # except BadSignature:
        #     return None  # invalid token
        except Exception:
            return None
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return 'User name=%s' % self.username


class Speaker(db.Model):
    __tablename__ = 'speaker'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    party = db.Column(db.String(100))
    state = db.Column(db.String(500))
    job = db.Column(db.String(100))
    true_cnt = db.Column(db.Integer())
    false_cnt = db.Column(db.Integer())
    pants_fire_cnt = db.Column(db.Integer())
    barely_true_cnt = db.Column(db.Integer())
    half_true_cnt = db.Column(db.Integer())
    mostly_true_cnt = db.Column(db.Integer())
    true_cnt_bin = db.Column(db.Integer())
    false_cnt_bin = db.Column(db.Integer())
    pub_news_cnt = db.Column(db.Integer())
    site_url = db.Column(db.String(500))


class Party(db.Model):
    __tablename__ = 'party'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))


class Metrics(db.Model):
    __tablename__ = 'metrics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(50))
    save_path = db.Column(db.String(100))
    mode = db.Column(db.Integer)
    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1 = db.Column(db.Float)
    sample_nums = db.Column(db.Integer)
    test_size = db.Column(db.Float)
    feature_dim = db.Column(db.Integer)
    training_times = db.Column(db.Integer, default=0)
    last_training_date = db.Column(db.DateTime)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statement = db.Column(db.String(500))
    speaker = db.Column(db.String(100))
    subjects = db.Column(db.String(100))
    pub_month = db.Column(db.String(15))
    pub_year = db.Column(db.String(15))
    label = db.Column(db.String(100))
    party = db.Column(db.String(50))


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(100))


class ML_result(db.Model):
    time = db.Column(DateTime, server_default=func.now(), primary_key=True)
    model = db.Column(db.String(10))
    feature_num = db.Column(db.Integer)
    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    fl = db.Column(db.Float)


def import_user():
    for i in range(1000, 3000, 3):
        user = User('jobs' + str(i) + '@gmail.com')
        user.hash_password('1')
        user.email = 'jobs' + str(i) + '@gmail.com'
        user.phone = '1786678' + str(i)
        db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.commit()
    import_user()
