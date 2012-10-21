# Pyap - The Python Audio Player Library
#
# Copyright (c) 2012 Joel Griffith
# Copyright (c) 2005 Joe Wreschnig
# Copyright (c) 2002 David I. Lehn
# Copyright (c) 2005-2011 the SQLAlchemy authors and contributors
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Unicode, MetaData
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import mapper, relationship, sessionmaker

from pyap.audio import Audio
from pyap.playlist import Playlist
from pyap.library import Library

def setup_db(uri):
    # TODO: echo should be false
    if uri is None:
        engine = create_engine('sqlite:///:memory:', echo=True)
    else:
        engine = create_engine('sqlite:///' + uri, echo=True)

    metadata = MetaData()

    #audio_types_table = Table('audio_types', metadata,
    #    Column('id', Integer, primary_key=True),
    #    Column('type', Unicode, unique=True)
    #)

    audio_table = Table('audio', metadata,
        Column('id', Integer, primary_key=True),
        Column('uri', Unicode, unique=True, index=True),
        Column('type', Integer, nullable=False),
        Column('artist', Unicode),
        Column('title', Unicode),
        Column('album', Unicode),
        Column('track', Integer),
        Column('length', Integer)
    )

    playlist_table = Table('playlists', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', Unicode, unique=True, index=True)
    )

    # many-to-many junction table for audio and playlists
    audio_playlist_table = Table('audio_playlists', metadata,
        Column('audio_id', Integer, ForeignKey('audio.id')),
        Column('playlist_id', Integer, ForeignKey('playlists.id'))
    )

    metadata.create_all(engine)

    mapper(Audio, audio_table)
    mapper(Playlist, playlist_table, properties={
        'audio': relationship(Audio, secondary=audio_playlist_table,
                                     backref='playlists')}
    )

    return sessionmaker(bind=engine)

class SQLAlchemyLibrary(Library):
    def __init__(self, uri=None):
        self.session_gen = setup_db(uri)

    def get_audios_where(self, **criteria=None):
        audios = self.session_gen().query(Audio)
        if criteria:
            audios = audios.filter_by(**criteria)
        return audios.all()

    def get_playlists_where(self, **criteria=None):
        playlists = self.session_gen().query(Playlist)
        if criteria:
            playlists = playlists.filter_by(**criteria)
        return playlists.all()

    def add_audios(self, audios):
        session = self.session_gen()
        session.add_all(audios)
        session.commit()

    def add_playlists(self, playlists):
        session = self.session_gen()
        # TODO: this should automatically add all Audio to the Library
        #       in the playlist that doesn't already exist
        # for audio in playlist:
        #     ...
        session.add_all(playlists)
        session.commit()

    def remove_audios(self, audios):
        session = self.session_gen()
        session.delete_all(audios)
        session.commit()

    def remove_playlists(self, playlists):
        session = self.session_gen()
        session.delete_all(playlists)
        session.commit()