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

import os

from mutagen import File

from pyap.util import get_extension
from pyap.audio import extensions

FILE = 0
STREAM = 1

class Audio(object):
    def __init__(self, uri, **kwargs):
        self.uri = unicode(uri)
        self.type = FILE
        self.artist = u''
        self.title = u''
        self.album = u''
        self.track = -1
        self.length = -1
        if kwargs:
            self.type = kwargs['type']
            self.artist = kwargs['artist']
            self.title = kwargs['title']
            self.album = kwargs['album']
            self.track = kwargs['track']
            self.length = int(kwargs['length'])
        else:
            if uri.startswith(r'http://'):
                self.type = STREAM
            elif get_extension(uri) in extensions.AUDIO:
                self.type = FILE
                if uri.find(os.sep):
                    self.uri = unicode(os.path.abspath(uri))
                filetype = File(self.uri, easy=True)
                self.length = int(filetype.info.length)
                if 'tracknumber' in filetype:
                    track = filetype['tracknumber'][0]
                    if track.find('/'):
                        self.track = int(track.split('/')[0])
                    else:
                        self.track = int(track)
                if 'artist' in filetype:
                    self.artist = unicode(" & ".join(filetype['artist']))
                if 'title' in filetype:
                    self.title = unicode(" ".join(filetype['title']))
                else:
                    filename = os.path.basename(self.uri)
                    self.title = unicode(os.path.splitext(filename)[0])
                if 'album' in filetype:
                    self.album = unicode(" ".join(filetype['album']))
            else:
                raise IOError("Not an audio file")

    def is_file(self):
        return self.type == FILE

    def is_stream(self):
        return self.type == STREAM

    # TODO: handle case where band name begins with "The" or other irrelevant words
    # FIXME: Shouldn't this just compare all relevant attributes at once? ie, title, artist, and album
    def cmp(self, audio, by='title'):
        if by == 'artist':
            return cmp(self.artist, audio.artist)
        elif by == 'title':
            return cmp(self.title, audio.title)
        elif by == 'album':
            return cmp(self.album, audio.album)
        return cmp(self.track, audio.track)

    def lt(self, audio, by='title'):
        return (self.cmp(audio, by) < 0)

    def gt(self, audio, by='title'):
        return (self.cmp(audio, by) > 0)

    def eq(self, audio, by='title'):
        return (self.cmp(audio, by) == 0)

    def __cmp__(self, audio):
        return self.cmp(audio)
        
    def __lt__(self, audio):
        return self.lt(audio)
      
    def __gt__(self, audio):
        return self.gt(audio)
          
    def __eq__(self, audio):
        return self.eq(audio)
        
    def __str__(self):
        if self.artist:
            return u"%s - %s" % (self.artist, self.title)
        return self.title

    def __repr__(self):
        id = ""
        if hasattr(self, 'id'):
            id = str(self.id)
        return u"<Audio('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
            id,
            "Stream" if self.is_stream() else "File",
            self.uri,
            self.artist,
            self.title,
            self.album,
            str(self.track),
            str(self.length)
        )
