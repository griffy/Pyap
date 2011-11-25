# Pyap - The Python Audio Player Library
#
# Copyright (c) 2011 Letat
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

from pyap.library.db import setup
from pyap.audio import Audio

Session = None

class Library(object):
    def __init__(self, uri=None):
        """ Not specifying a URI results in an in-memory library """
        global Session
        if Session is None:
            Session = setup(uri)

    def audio_by_index(self, index):
        return Session().query(Audio).filter_by(id=index).first()

    def audio_by_uri(self, uri):
        return Session().query(Audio).filter_by(uri=uri).first()

    def all_audio(self):
        return Session().query(Audio).order_by(Audio.id).all()

    def playlist_by_name(self, name):
        return Session().query(Playlist).filter_by(name=name).first()
        
    def add_audio(self, audio):
        session = Session()
        if isinstance(audio, list) and isinstance(audio[0], Audio):
            session.add_all(audio)
            session.commit()
        elif isinstance(audio, Audio):
            session.add(audio)
            session.commit()

    def remove_audio(self, audio):
        session = Session()
        if isinstance(audio, list) and isinstance(audio[0], Audio):
            session.delete_all(audio)
            session.commit()
        elif isinstance(audio, Audio):
            session.delete(audio)
            session.commit()

    def add_audio_by_uri(self, uri):
        session = Session()
        if isinstance(uri, list) and isinstance(uri[0], str):
            session.add_all([Audio(u) for u in uri])
            session.commit()
        else:
            session.add(Audio(uri))
            session.commit()

    def remove_audio_by_uri(self, uri):
        session = Session()
        if isinstance(uri, list) and isinstance(uri[0], str):
            session.delete_all([Audio(u) for u in uri])
            session.commit()
        else:
            session.delete(Audio(uri))
            session.commit()

    def add_playlist(self, playlist):
        session = Session()
        # TODO: this should automatically add all Audio to the Library
        #       in the playlist that doesn't already exist
        #for audio in playlist:
        #    playlist.audio.append(audio)
        session.add(playlist)
        session.commit()

    def remove_playlist(self, playlist):
        session = Session()
        session.delete(playlist)
        session.commit()

