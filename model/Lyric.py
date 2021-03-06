# coding: utf-8
from SinglePage.general_view_with_sqlalchemy import GeneralViewWithSQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from .Base import Base, db_session


class Lyric(GeneralViewWithSQLAlchemy, Base):

    db_session = db_session
    __tablename__ = 'Lyric'

    id = Column(Integer, primary_key=True)
    file_path = Column(String(500))

    songinfo = relationship("SongInfo", back_populates='lyrics')

    __property__ = {}
    __in_exclude__ = ['id']
    __exclude__ = ['songinfo']
    __permission__ = []
