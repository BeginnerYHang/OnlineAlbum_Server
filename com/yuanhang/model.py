# 创建对象的基类
from enum import Enum

from sqlalchemy import Column, INT, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/online_album')
DBSession = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'user'
    id = Column(INT, primary_key=True, nullable=False, autoincrement=True)
    uname = Column(String(32), nullable=False)
    password = Column(String(256))

    #  一的一方写relationship,可以通过表名.字段得到一个列表
    #  多的一方写ForeignKey,可以通过表名.(一的一方的backref)对一的一方进行读取和修改'''
    photos = relationship('Photo')

    def __init__(self, uname, password):
        self.uname = uname
        self.password = password


class Photo(Base):
    __tablename__ = 'photo'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(INT, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(256), nullable=False)
    uid = Column(INT, ForeignKey('user.id'))

    def __init__(self, name, uid):
        self.name = name
        self.uid = uid


#  添加用户
def add_user(uname, password):
    session = DBSession()
    user = User(uname, password)
    session.add(user)
    session.flush()
    # flush后可以获得插入后的uid
    id = user.id
    session.commit()
    session.close()
    return id


def find_user_by_name(uname):
    session = DBSession()
    count = session.query(User).filter_by(uname=uname).count()
    session.close()
    return count


# 判断用户是否登录成功
def find_user(uname, password):
    session = DBSession()
    user = session.query(User).filter_by(uname=uname, password=password).first()
    session.close()
    return user

def save_photo(photo_name, uid):
    photo = Photo(photo_name, uid)
    session = DBSession()
    session.add(photo)
    session.commit()
    session.close()


def find_photos_by_uid(uid):
    session = DBSession()
    photos = session.query(Photo).filter_by(uid=uid).all()
    if photos is None:
        return []
    return photos



class Message(object):

    #  描述请求信息的类,status为"ok/error",ok则携带数据data,error则传入错误描述description
    #  python支持实例自定义属性
    def __init__(self, status=1):
        self.status = status

if __name__ == '__main__':
    add_user("aaa","bbb")