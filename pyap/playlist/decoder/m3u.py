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

from pyap.playlist.decoder import Decoder
from pyap.playlist import Playlist
from pyap.audio import Audio

# TODO: Decide whether to ignore EXTINFOs when creating Audio objects
#       If it's a stream, it should not be ignored
class M3UDecoder(Decoder):
    def decode(self, playlist_uri):
        playlist = Playlist()
        extended = False
        file = open(playlist_uri, 'r')
        if file.readline().lower().startswith('#EXTM3U'):
            extended = True

        if extended:
            # Parse it as an extended M3U file
            info = (0, "")
            for line in file.readlines():
                line = line.replace('\n', '')
                if line.startswith('#'):
                    if line.startswith('#EXTINF'):
                        length, title = line.split("#EXTINF:", 1)[1].split(",", 1)
                        info = (int(length), title)
                else:
                    uri = line
                    if not (uri.startswith(os.sep) or uri[1] == ':'):
                        directory_uri = os.path.dirname(playlist_uri)
                        uri = os.path.join(directory_uri, uri)
                    self.add(playlist, uri)
        else:
            # Parse it as a generic M3U file
            for line in file.readlines():
                line = line.replace('\n', '')
                if line.startswith('#'):
                    continue
                uri = line
                if not (uri.startswith(os.sep) or uri[1] == ':'):
                    directory_uri = os.path.dirname(playlist_uri)
                    uri = os.path.join(directory_uri, uri)
                self.add(playlist, uri)

        file.close()
        return playlist


def add(playlist, uri):
    try:
        get_extension(uri)
        add_file(playlist, uri)
    except ValueError:
        add_directory(playlist, uri)

def add_directory(playlist, uri):
    for root, dirs, files in os.walk(uri):
        for file in files:
            add_file(playlist, os.path.join(root, file))

def add_file(playlist, uri):
    try:
        playlist.append(Audio(uri))
    except IOError: pass


