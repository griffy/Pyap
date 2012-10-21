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

from pyap.audio import Audio
from pyap.playlist import Playlist

class Library(object):
    """ Interface that implementers must satisfy to be
        considered a Library
    """
    def __init__(self, uri=None):
        """ When no URI is given, the library should be in-memory """
        raise NotImplementedError()

    def get_audios_where(self, **criteria=None):
        """ When no criteria is given, all audio should be returned """
        raise NotImplementedError()
        
    def get_playlists_where(self, **criteria=None):
        """ When no criteria is given, all playlists should be returned """
        raise NotImplementedError()

    def add_audios(self, audios):
        raise NotImplementedError()

    def add_playlists(self, playlists):
        raise NotImplementedError()

    def remove_audios(self, audios):
        raise NotImplementedError()

    def remove_playlists(self, playlists):
        raise NotImplementedError()

    def generate_playlist(self):
        return Playlist('default', self.get_audios())

    def get_audios(self):
        return self.get_audios_where()
   
    def get_playlists(self):
        return self.get_playlists_where()

    def get_first_audio_where(self, **criteria):
        audios = self.get_audios_where(**criteria)
        if not audios:
            return None
        return audios[0]

    def get_first_playlist_where(self, **criteria):
        playlists = self.get_playlists_where(**criteria)
        if not playlists:
            return None
        return playlists[0]

    def add_audio(self, audio):
        self.add_audios([audio])

    def add_playlist(self, playlist):
        self.add_playlists([playlist])

    def remove_audio(self, audio):
        self.remove_audios([audio])

    def remove_playlist(self, playlist):
        self.remove_playlists([playlist])

