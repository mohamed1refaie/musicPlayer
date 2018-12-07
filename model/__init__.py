from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///db/song.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

from model.artist import Artist
from model.song import Song
from model.playlist import Playlist
from model.album import Album

# Create new tables
Base.metadata.create_all(engine)