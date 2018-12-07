from model import *
from mutagen.mp3 import MP3


def main():
    menu = """
-------------------------------------
|                                    |
|   1:  Add Song                     |       
|   2:  Create Playlist              |
|   3:  View Songs                   |
|   4:  View Play Lists              |
|   5:  View Artists                 |
|   6:  View Albums                  |
|   7:  Play Song                    |
|   8:  Play Playlist                |
|   9:  Play Artist Songs            |
|   10: Play Album                   |
|   11: Play Genre                   |
|   12: Remove song from playlist    |
|   13: Delete Playlist              |
|   14: Delete Song                  |
|   15: Delete Album                 |
|   16: Delete Artist                |
|   0:  exit                         |
|                                    |
-------------------------------------

"""

    while True:
        res = int(input(menu))
        if res == 1:
            song = Song()
            song.name = input('Song Name: ')

            song_files = Song.view_files()
            file_id = int(input('Select song file: '))
            song.path = 'db/songs/%s' % song_files[file_id - 1]
            audio = MP3(song.path)
            secs = round(audio.info.length)
            minutes = (secs // 60)
            secs %= 60
            secs= round(secs)
            song.duration = str(minutes) + ":" + str(secs)
            print("Duration: ",song.duration)
            song.genre = input('Genre: ')
            song.release_date = input('Release Date: ')
            artist_list = session.query(Artist).order_by(Artist.name).all()

            print('Select an artist:')
            print('0: Add new artist')
            for i, artist in enumerate(artist_list):
                print('%s: %s' % (i + 1, artist.name))

            res = int(input())
            if (res == 0):
                artist = Artist()
                artist.name = input('Artist Name: ')
                artist.songs = [song]
                session.add(artist)
            else:
                artist_list[res - 1].songs.append(song)
                session.add(artist_list[res - 1])

            album_name = input('Album Name: ')
            album = Album.find_or_create(album_name)
            album.songs.append(song)
            session.add(album)

            session.commit()
        elif res == 2:
            Playlist.create_playlist()
        elif res == 3:
            song=Song.select_song()
            print("Song: ",song.name)
            print("Artist: ",song.artist)
            print("Album: ",song.album.name)
            print("Release Date: ",song.release_date)
            print("Duration: ",song.duration)
            print("Genre: ",song.genre)
        elif res == 4:
            playlist = Playlist.select_playlist()
            if playlist is not None:
                print(playlist)
                input()
        elif res == 5:
            Artist.view_artists()
            input()
        elif res == 6:
            Album.view_albums()
        elif res == 7:
            Song.play_song()
        elif res == 8:
            Playlist.select_and_play()
        elif res == 9:
            artists = Artist.view_artists()
            artist_id = int(input('Select Artist(0 back): '))
            if artist_id > 0:
                artists[artist_id - 1].play_all()
        elif res == 10:
            Album.select_and_play()
        elif res == 11:
            Song.play_genre()
        elif res == 12:
            playlist = Playlist.select_playlist()
            if playlist is not None:
                playlist.remove_song()
        elif res == 13:
            playlist = Playlist.select_playlist()
            if playlist is not None:
                playlist.delete()
        elif res == 14:
            song = Song.select_song()
            if song is not None:
                song.delete()
        elif res == 15:
            album = Album.select_album()
            if album is not None:
                album.delete()
        elif res == 16:
            artist = Artist.select_artist()
            if artist is not None:
                artist.delete()
        elif res == 17:
            playlist = Playlist.select_playlist()
            if playlist is not None:
                print("sd")
        elif res == 0:
            break


if __name__ == "__main__":
    main()