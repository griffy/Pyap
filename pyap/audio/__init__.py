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
UNKNOWN = 2

def uri_type(uri):
    if uri.startswith(r'http://'):
        return STREAM
    elif get_extension(uri) in extensions.AUDIO:
        return FILE
    return UNKNOWN

def audio_info(uri):
    info = {
        'length': -1,
        'track': -1,
        'year': u''
        'artist': u'',
        'title': unicode(os.path.splitext(os.path.basename(uri))[0]),
        'album': u''
    }
    
    audio_file = File(uri, easy=True)
    info['length'] = int(audio_file.info.length)

    if 'tracknumber' in audio_file:
        track = audio_file['tracknumber'][0]
        if track.find('/'):
            track = int(track.split('/')[0])
        else:
            track = int(track)
        info['track'] = track

    if 'date' in audio_file:
        info['year'] = audio_file['date']

    if 'artist' in audio_file:
        info['artist'] = unicode(" & ".join(audio_file['artist']))
    
    if 'title' in audio_file:
        info['title'] = unicode(" ".join(audio_file['title']))

    if 'album' in audio_file:
        info['album'] = unicode(" ".join(audio_file['album']))

    return info


class Audio(object):
    def __init__(self, uri, **kwargs):
        self.type = kwargs['type'] if kwargs['type'] else UNKNOWN
        self.artist = kwargs['artist'] if kwargs['artist'] else u''
        self.title = kwargs['title'] if kwargs['title'] else u''
        self.album = kwargs['album'] if kwargs['album'] else u''
        self.track = int(kwargs['track']) if kwargs['track'] else -1
        self.length = int(kwargs['length']) if kwargs['length'] else -1
        self.year = kwargs['year'] if kwargs['year'] else u''

        if self.type == UNKNOWN:
            self.type = uri_type(self.uri)

        self.uri = unicode(uri)
        if self.type == FILE and uri.find(os.sep):
            self.uri = unicode(os.path.abspath(uri))

        if not kwargs:
            # analyze the track ourselves if no info was given
            self.update(audio_info(uri))

    def update(self, audio_info):
        if 'length' in audio_info:
            self.length = audio_info['length']
        if 'track' in audio_info:
            self.track = audio_info['track']
        if 'year' in audio_info:
            self.year = audio_info['year']
        if 'artist' in audio_info:
            self.artist = audio_info['artist']
        if 'title' in audio_info:
            self.title = audio_info['title']
        if 'album' in audio_info:
            self.album = audio_info['album']

    def is_file(self):
        return self.type == FILE

    def is_stream(self):
        return self.type == STREAM

    # TODO: handle case where band name begins with "The" or other irrelevant words
    def __cmp__(self, audio):
        if self.artist and audio.artist:
            if self.artist == audio.artist:
                if self.album and audio.album:
                    if self.album == audio.album:
                        if self.track != -1 and audio.track != -1:
                            return cmp(self.track, audio.track)
                        else:
                            return cmp(self.title, audio.title)
                    else:
                        if self.year and audio.year:
                            return cmp(self.year, audio.year)
                        else:
                            return cmp(self.album, audio.album)
                else:
                    return cmp(self.title, audio.title) 
            else:
                return cmp(self.artist, audio.artist)

        return cmp(self.title, audio.title) 
        
    def __str__(self):
        if self.artist:
            return u"%s - %s" % (self.artist, self.title)
        return self.title

    def __repr__(self):
        id = ""
        if hasattr(self, 'id'):
            id = str(self.id)
        return u"<Audio('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
            id,
            "Stream" if self.is_stream() else "File",
            self.uri,
            self.artist,
            self.title,
            self.album,
            str(self.track),
            str(self.length),
            self.year
        )
