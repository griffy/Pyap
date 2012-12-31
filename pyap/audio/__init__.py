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

import os

from mutagen import File

from pyap.util import get_extension, is_audio

FILE = 0
STREAM = 1
UNKNOWN = 2

def uri_type(uri):
    if uri.startswith(r'http://'):
        return STREAM
    extension = get_extension(uri)
    if extension and is_audio(extension):
        return FILE
    return UNKNOWN

def audio_info(uri):
    info = {
        'length': -1,
        'track': -1,
        'year': u'',
        'artist': u'',
        'title': unicode(os.path.splitext(os.path.basename(uri))[0]),
        'album': u''
    }
    
    audio_file = File(uri, easy=True)
    if not audio_file:
        return None

    info['length'] = int(audio_file.info.length)

    if 'tracknumber' in audio_file:
        track = audio_file['tracknumber'][0]
        if track.find('/'):
            track = int(track.split('/')[0])
        else:
            track = int(track)
        info['track'] = track

    if 'date' in audio_file:
        info['year'] = unicode(", ".join(audio_file['date']))

    if 'artist' in audio_file:
        info['artist'] = unicode(" & ".join(audio_file['artist']))
    
    if 'title' in audio_file:
        info['title'] = unicode(", ".join(audio_file['title']))

    if 'album' in audio_file:
        info['album'] = unicode(", ".join(audio_file['album']))

    return info


class Audio(object):
    """ Note: Title attribute will never be blank """
    def __init__(self, uri, **kwargs):
        self.type = kwargs['type'] if 'type' in kwargs else UNKNOWN
        self.artist = kwargs['artist'] if 'artist' in kwargs else u''
        self.title = kwargs['title'] if 'title' in kwargs else u''
        self.album = kwargs['album'] if 'album' in kwargs else u''
        self.track = int(kwargs['track']) if 'track' in kwargs else -1
        self.length = int(kwargs['length']) if 'length' in kwargs else -1
        self.year = kwargs['year'] if 'year' in kwargs else u''

        if self.type == UNKNOWN:
            self.type = uri_type(uri)

        self.uri = unicode(uri)
        if self.is_file():
            if self.uri.find(os.sep):
                self.uri = unicode(os.path.abspath(self.uri))

            if not kwargs:
                # analyze the track ourselves if no info was given
                info = audio_info(self.uri)
                if info is None:
                    raise Exception("Not an audio file")
                self.update(**info)
        elif self.is_stream():
            if not self.title:
                self.title = "Stream: %s" % self.uri

        self.player = None

    def update(self, **kwargs):
        if 'length' in kwargs:
            self.length = kwargs['length']
        if 'track' in kwargs:
            self.track = kwargs['track']
        if 'year' in kwargs:
            self.year = kwargs['year']
        if 'artist' in kwargs:
            self.artist = kwargs['artist']
        if 'title' in kwargs:
            self.title = kwargs['title']
        if 'album' in kwargs:
            self.album = kwargs['album']

    # FIXME: the on_finish function should only 
    #        be part of the player until the audio
    #        file is done playing, and not remain
    #        on the player (as it does now)
    def play(self, player=None, rate=None, on_finish=None):
        if not player:
            from pyap.player import Player
            self.player = Player(on_finish=on_finish)
        else:
            self.player = player
            if on_finish is not None:
                self.player.connect('audio_finished', on_finish)
        def cleanup_player(audio):
            audio.stop()
        self.player.connect('audio_finished', cleanup_player)
        self.player.play(self, rate=rate)

    def pause(self):
        if self.player is not None:
            self.player.pause()

    def resume(self):
        if self.player is not None:
            self.player.resume()

    def stop(self):
        if self.player is not None:
            self.player.stop()
            self.player = None

    def is_playing(self):
        if self.player is None:
            return False
        return self.player.is_playing()

    def is_streaming(self):
        if self.player is None:
            return False
        return self.player.is_streaming()

    def is_paused(self):
        if self.player is None:
            return False
        return self.player.is_paused()

    def is_stopped(self):
        if self.player is None:
            return True
        return self.player.is_stopped()

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
