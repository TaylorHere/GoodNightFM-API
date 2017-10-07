# coding: utf-8
from .Base import Base, db_session

from SinglePage.general_view_with_sqlalchemy import GeneralViewWithSQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime,timedelta


class SongInfo(GeneralViewWithSQLAlchemy, Base):

    db_session = db_session
    __tablename__ = 'SongInfo'

    id = Column(Integer, primary_key=True)
    title = Column(String(140))
    subtitle = Column(String(200))
    update_time = Column(DateTime())
    song_id = Column(Integer, ForeignKey('Song.id'))
    cover_id = Column(Integer, ForeignKey('Cover.id'))
    lyric_id = Column(Integer, ForeignKey('Lyric.id'))

    songs = relationship("Song", back_populates='songinfo')
    covers = relationship("Cover", back_populates='songinfo')
    lyrics = relationship("Lyric", back_populates='songinfo')

    def post(self, *args, **kwargs):
        self.update_time = datetime.now()
        return super(SongInfo, self).post(args, kwargs)

    def day(self, instance, query, value):
        query = query.filter(SongInfo.update_time != None)
        query = query.filter(SongInfo.update_time.between(datetime.now()-timedelta(days=int(value)),datetime.now()))
        return query

    def add_args(self):
        # 增加no_expired过滤器
        super(SongInfo, self).__query_args__.append({'day': self.day})

    __property__ = {}
    __in_exclude__ = ['id', 'update_time']
    __exclude__ = ['songinfo']
    __permission__ = []
