'''Data controller'''
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from db_model import User
import db_model
from _mysql_exceptions import IntegrityError

Session = sessionmaker()

class SQLEngine(object):
    '''SQL Engine Class'''
    engine = None
    session = None
    __user__ = 'root'
    __password__ = ''
    __host__ = 'localhost'
    __port__ = '5000'
    __db_name__ = 'demo'
    def __init__(self):
        '''Create database engine.'''
        #self.engine = create_engine('mysql://{0}:{1}@{2}:{3}'.format(user, password, host, port))
        self.engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(
            self.__user__, self.__password__, self.__host__,
            self.__port__, self.__db_name__))
        Session.configure(bind=self.engine)
        self.session = Session()
        db_model.initialize_datamodel(self.engine)

    def add_user(self, username, email, password):
        '''Add user to database.'''
        new_user = User(username=username,
                        email=email,
                        password=password)
        is_valid_entry = self.check_valid_entry(new_user.username, new_user.email)
        if is_valid_entry:
            try:
                self.session.add(new_user)
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                return False
            return True
        return False

    def check_login(self, username, password):
        '''Check login for user'''
        valid_user = self.get_user_by_username(username) #Get user with username
        if valid_user: #User is available
            if valid_user.verify_password(password): #Verify password
                return True
        return False

    def check_valid_entry(self, username, email):
        '''Check valid entry before adding user'''
        existed_user = self.session.query(User).filter(
            or_(
                User.username == username,
                User.email == email)
            ).first()
        if existed_user:
            return False
        return True

    def get_user_by_email(self, email):
        '''Check duplicate email'''
        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username):
        '''Search user by username'''
        return self.session.query(User).filter(User.username == username).first()
