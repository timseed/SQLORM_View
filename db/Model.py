from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref, Query

from db import Base
from db.View import CreateView, create_view


class UserChannel(Base):
    __tablename__ = "userchannel"
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    channel_id = Column(Integer, ForeignKey("channel.channel_id"), primary_key=True)
    # Name              Classname
    user = relationship("User", backref=backref("tv", cascade="all, delete-orphan"))
    channel = relationship("Channel", backref=backref("tv", cascade="all, delete-orphan"))


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(20))
    channels = relationship("Channel", secondary="userchannel")


class Channel(Base):
    __tablename__ = 'channel'
    channel_id = Column(Integer,
                        autoincrement=True,
                        primary_key=True)
    name = Column(String(20))
    users = relationship("User", secondary="userchannel")


class PCVIEW_MV(CreateView):
    from db import use_db
    session = use_db()
    q = Query([User, Channel, UserChannel], session=session). \
        filter(User.user_id == UserChannel.user_id). \
        filter(Channel.channel_id == UserChannel.channel_id). \
        with_entities(User.name.label('uname'), Channel.name.label('cname'))
    sqlcmd = str(q.selectable)
    junk = 1
    print(f"{sqlcmd}")
    __tablename__ = create_view("pc_view_mv", q.selectable)
