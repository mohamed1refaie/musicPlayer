from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from . import Base, Song, session


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    songs = relationship('Song', back_populates='album')

    def __init__(self, name):
        self.name = name

    def play(self):
        for song in self.songs:
            song.play()

    def delete(self):
        for song in self.songs:
            song.delete()
        session.delete(self)
        session.commit()

    @staticmethod
    def find_or_create(name):
        album = session.query(Album).filter_by(name=name).first()
        if album is None:
            album = Album(name)
        return album

    @staticmethod
    def select_and_play():
        albums = Album.get_all()
        for i, album in enumerate(albums):
            print('%s: %s' % (i + 1, album.name))
        album_id = int(input('Select Album (0 back): '))
        albums[album_id - 1].play()

    @staticmethod
    def get_all():
        return session.query(Album).order_by(Album.name).all()

    @staticmethod
    def select_album():
        albums = Album.get_all()
        for i, album in enumerate(albums):
            print('%s: %s' % (i + 1, album.name))

        album_id = int(input('Select Album (0 back): '))
        if album_id > 0:
            return albums[album_id - 1]

    @staticmethod
    def view_albums():
        albums = Album.get_all()
        for i, album in enumerate(albums):
            print('%s: %s' % (i + 1, album.name))

        album_id = int(input('Select Album (0 back): '))
        if album_id > 0:
            print(albums[album_id - 1])
            input()

    @staticmethod
    def create_album():
        name = input('Album Name: ')
        album = Album(name)
        album.desc = input('Album Desc: ')

        songs = Song.get_all()
        for i, song in enumerate(songs):
            print('%s: %s' % (i + 1, song))
        while True:
            song_id = int(input('Song id (0 to finish): '))
            if song_id == 0:
                break
            album.songs.append(songs[song_id - 1])

        session.add(album)
        session.commit()

    def __repr__(self):
        ret = 'Album:\n'
        ret += 'Name: %s\n' % self.name
        ret += 'Songs:'
        for song in self.songs:
            ret += '\n\t%s   Duration: %s' % (song.name,song.duration)
        return ret