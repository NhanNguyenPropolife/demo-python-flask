'''Data model for web application'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text
import bcrypt

BASE = declarative_base()

class User(BASE):
    '''User table'''
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(length=80), nullable=False, unique=True)
    email = Column(String(length=80), nullable=False, unique=True)
    password = Column(Text)

    def __repr__(self):
        return "<User(username='{0}', email='{1}', password='{2}')>".format(
            self.username, self.email, self.password)

    def __str__(self):
        return self.__repr__()

    def verify_password(self, password):
        """Verify password for User"""
        pwhash = bcrypt.hashpw(password.encode(encoding='utf-8'), self.password)
        return self.password == pwhash

def initialize_datamodel(engine):
    """Create tables if necessary"""
    BASE.metadata.create_all(engine)
    