import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key = True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    return Session()

def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all() # формирует список альбомов данного исполнителя
    return albums

def add_album(album):
    """
    Добавляет уникальный альбом в БД
    """
    session = connect_db()
    new_album = Album(
        year = album["year"],
        artist = album["artist"],
        genre = album["genre"],
        album = album["album"]
        )
    albums_ = session.query(Album).filter(Album.artist == album["artist"], Album.album == album["album"]) # проверка на уникальность альбома у исполнителя
    albums_cnt = albums_.count()
    if albums_cnt==0:
        session.add(new_album)
        session.commit()
        message = ("Альбом {} исполнителя {} добавлен в БД!".format(album["album"], album["artist"]))
    else:
        session.commit()
        message = ("Альбом {} исполнителя {} уже есть в БД!".format(album["album"], album["artist"]))
    return message, albums_cnt
