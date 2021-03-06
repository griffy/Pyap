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
import time
import threading

import gobject
import pygst
pygst.require("0.10")
import gst

from pyap.util import EventGenerator

STREAMING = 0
STOPPED = 1
PLAYING = 2
PAUSED = 3

class Player(EventGenerator):
    gobject_loop_context = None

    def __init__(self, create_gobject_loop=True, on_finish=None):
        EventGenerator.__init__(self)
        self._player = gst.element_factory_make('playbin2', 'player')
        fakesink = gst.element_factory_make('fakesink', 'fakesink')
        self._player.set_property('video-sink', fakesink)
        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_bus_message)
        self.reset()
        if on_finish is not None:
            self.connect('audio_finished', on_finish)
        if create_gobject_loop and self.gobject_loop_context is None:
            loop = gobject.MainLoop()
            gobject.threads_init()
            self.gobject_loop_context = loop.get_context()

    def loop_gobject_context(self):
        # if we have a gobject loop context, force
        # it to iterate until the audio we're playing
        # has stopped
        if self.gobject_loop_context is None:
            return

        while not self.is_stopped():
            self.gobject_loop_context.iteration(True)
    
    def reset(self):
        # TODO: should all callbacks be cleared?
        self._player.set_state(gst.STATE_NULL)
        self._state = STOPPED
        self._current_audio = None
        
    def play(self, audio, rate=None):
        self.play_uri(audio.uri, stream=audio.is_stream(), rate=rate)
        self._current_audio = audio
        
    def play_uri(self, uri, stream=False, rate=None):
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
        self.set_position(0, playback_rate=rate)
        # in this case, current audio will just be the string uri
        self._current_audio = uri
        # spawn a thread that loops the gobject context so we can
        # continue to receive events on the bus
        threading.Thread(group=None, target=self.loop_gobject_context).start()
    
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

    def set_position(self, time, playback_rate=None):
        if self.is_streaming() or self.is_stopped():
            return

        if time <= 0:
            pos = 0
        elif time > self.audio_duration():
            pos = self.audio_duration() * 1000000000
        else:
            pos = time * 1000000000

        if playback_rate is None:
            self._player.seek_simple(gst.FORMAT_TIME,
                                     gst.SEEK_FLAG_FLUSH,
                                     pos)
        else:
            self._player.seek(playback_rate, 
                              gst.FORMAT_TIME,
                              gst.SEEK_FLAG_FLUSH,
                              gst.SEEK_TYPE_SET,
                              pos,
                              gst.SEEK_TYPE_SET,
                              self.audio_duration()*1000000000)

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
            finished_audio = self.current_audio()
            self.stop()
            self.emit('audio_finished', finished_audio)
            
