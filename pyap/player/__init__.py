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
import time

import pygst
pygst.require("0.10")
import gst

from pyap.util import Event

STREAMING = 0
STOPPED = 1
PLAYING = 2
PAUSED = 3
    
class Player(object):
    def __init__(self):
        self._player = gst.element_factory_make('playbin2', 'player')
        fakesink = gst.element_factory_make('fakesink', 'fakesink')
        self._player.set_property('video-sink', fakesink)
        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_bus_message)
        self.reset()

    def connect(self, event, func):
        if event == 'audio_ended':
            self._finished_func = func
            
    def reset(self):
        self._player.set_state(gst.STATE_NULL)
        self._state = STOPPED
        self._current_audio = None
        self.set_volume(0.5)
        self._finished_func = None
        
    def play(self, audio):
        self.play_uri(audio.uri, audio.is_stream())
        self._current_audio = audio
        
    def play_uri(self, uri, stream=False):
        self.stop()
        if stream:
            self._player.set_property("uri", uri)
            self._state = STREAMING
        else:
            if os.name == 'nt':
                self._player.set_property("uri", uri)
            else:
                self._player.set_property("uri", "file://" + uri)
            self._state = PLAYING
        self._player.set_state(gst.STATE_PLAYING)
        # in this case, current audio will just be the string uri
        self._current_audio = uri
        
    def pause(self):
        if (self._state == PLAYING or
            self._state == STREAMING):
            self._player.set_state(gst.STATE_PAUSED)
            self._state = PAUSED

    def resume(self):
        if self._state == PAUSED:
            self._player.set_state(gst.STATE_PLAYING)
            self._state = PLAYING

    def stop(self):
        if self._state != STOPPED:
            self._player.set_state(gst.STATE_NULL)
            self._state = STOPPED
            self._current_audio = None
            
    def is_playing(self):
        return self._state == PLAYING

    def is_streaming(self):
        return self._state == STREAMING

    def is_paused(self):
        return self._state == PAUSED

    def is_stopped(self):
        return self._state == STOPPED

    def set_position(self, time):
        if not self.is_streaming():
            if time <= 0:
                self._player.seek_simple(gst.FORMAT_TIME,
                                         gst.SEEK_FLAG_FLUSH,
                                         0)
            elif time > self.audio_duration():
                self._player.seek_simple(gst.FORMAT_TIME,
                                         gst.SEEK_FLAG_FLUSH,
                                         self.audio_duration()*1000000000)
            else:
                self._player.seek_simple(gst.FORMAT_TIME,
                                         gst.SEEK_FLAG_FLUSH,
                                         time*1000000000)

    def position(self):
        if self.is_streaming():
            return -1
        if self._player.get_state() != gst.STATE_NULL:
            pos = int(self._player.query_position(gst.FORMAT_TIME, None)[0])
            return pos / 1000000000
        return -1

    def audio_duration(self):
        if self.is_streaming():
            return -1
        if self._player.get_state() != gst.STATE_NULL:
            pos = int(self._player.query_duration(gst.FORMAT_TIME, None)[0])
            return pos / 1000000000
        return -1

    def progress(self):
        """ Convenience method to get a tuple of player's position and audio
            duration """
        return (self.position(), self.audio_duration())

    def current_audio(self):
        return self._current_audio
        
    def set_volume(self, volume):
        self._player.set_property('volume', volume)

    def volume(self):
        return self._player.get_property('volume')

    def _on_bus_message(self, bus, message):
        if (message.type == gst.MESSAGE_EOS or
            message.type == gst.MESSAGE_ERROR):
            self.stop()
            if self._finished_func:
                self._finished_func(self.current_audio())
