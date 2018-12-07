from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
from . import Base, Song, session

playlist_song = Table('playlist_song', Base.metadata,
                      Column('playlist_id', Integer,
                             ForeignKey('playlists.id')),
                      Column('song_id', Integer, ForeignKey('songs.id')))


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    songs = relationship('Song', secondary=playlist_song)

    def play(self):
        for song in self.songs:
            song.play()

    def remove_song(self):
        song = self.select_song()
        if song is not None:
            self.songs.remove(song)
            session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    def select_song(self):
        for i, song in enumerate(self.songs):
            print('%s: %s' % (i + 1, song))
        song_id = int(input('Select song to remove (0 back): '))
        if song_id > 0:
            return self.songs[song_id - 1]

    @staticmethod
    def select_and_play():
        playlists = Playlist.get_all()
        for i, playlist in enumerate(playlists):
            print('%s: %s' % (i + 1, playlist.name))
        playlist_id = int(input('Select Playlist (0 back): '))
        playlists[playlist_id - 1].play()

    @staticmethod
    def get_all():
        return session.query(Playlist).order_by(Playlist.name).all()

    @staticmethod
    def select_playlist():
        playlists = Playlist.get_all()
        for i, playlist in enumerate(playlists):
            songs=str(playlist.songs)
            tracknos=songs.count('-')
            print('%s: %s        Tracks: %s' % (i + 1, playlist.name,tracknos))

        playlist_id = int(input('Select Playlist (0 back): '))
        if playlist_id > 0:
            return playlists[playlist_id - 1]

    @staticmethod
    def create_playlist():
        playlist = Playlist()
        playlist.name = input('Playlist Name: ')
        playlist.desc = input('Playlist Desc: ')

        songs = Song.get_all()
        for i, song in enumerate(songs):
            print('%s: %s' % (i + 1, song))
        while True:
            song_id = int(input('Song id (0 to finish): '))
            if song_id == 0:
                break
            playlist.songs.append(songs[song_id - 1])

        session.add(playlist)
        session.commit()

    def add_songs(self):
        songs = Song.get_all()
        for i, song in enumerate(songs):
            print('%s: %s' % (i + 1, song))
        while True:
            song_id = int(input('Song id (0 to finish): '))
            if song_id == 0:
                break
            self.songs.append(songs[song_id - 1])

        session.merge(self)
        session.commit()


    def __repr__(self):
        ret = 'Playlist:\n'
        ret += 'Name: %s\n' % self.name
        ret += 'Desc: %s\n' % self.desc
        ret += 'Songs:'
        for song in self.songs:
            ret += '\n\t%s   Duration: %s' % (song.name,song.duration)
        return ret