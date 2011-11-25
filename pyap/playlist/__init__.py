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

import random

from pyap.util import get_extension
from pyap.playlist.decoder import get_decoder
from pyap.playlist.encoder import get_encoder
from pyap.audio import Audio

REPEAT_ONE = 0
REPEAT_ALL = 1
REPEAT_OFF = 2

# imports a playlist in a different format (.m3u, .pls, etc.) and returns
# a Playlist object
def import_playlist(playlist_uri):
    ext = get_extension(playlist_uri)
    decoder = get_decoder(ext)
    return decoder.decode(playlist_uri)

# TODO: add a history of played audio so that when a user manually
#       selects an audio, using previous() will make sense

class Playlist(object):
    def __init__(self, name, audio_list=[]):
        self.name = name
        self._audio_list = audio_list
        self.reset()
        
    def reset(self):
        self.current_index = 0
        self.set_shuffle(False)
        self.set_repeat(REPEAT_ALL)
        self._reorder()
        
    def _reorder(self):
        if self.is_shuffling():
            self._order = random.shuffle(range(len(self._audio_list)))
        else:
            self._order = range(len(self._audio_list))
            
    def __len__(self):
        return len(self._audio_list)
        
    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            return [self._audio_list[i] for i in range(*indices)]
        else:
            if index < 0:
                # Negative index means start from the end
                return self._audio_list[len(self)+index]
            if 0 <= index < len(self):
                return self._audio_list[index]
            
    def __setitem__(self, index, audio):
        if 0 <= index < len(self):
            self._audio_list[index] = audio
                
    def __delitem__(self, index):
        if 0 <= index < len(self):
            del self._audio_list[index]
            self._reorder()
            
    def __iter__(self):
        for audio in self._audio_list:
            yield audio
            
    def __contains__(self, audio):
        return audio in self._audio_list
        
    def append(self, audio):
        self._audio_list.append(audio)
        self._reorder()
        
    def extend(self, audio_list):
        self._audio_list.extend(audio_list)
        self._reorder()
            
    def remove(self, audio):
        index = self.index(audio)
        del self[index]
            
    def pop(self, index=None):
        if index is None:
            index = len(self)-1
        if 0 <= index < len(self):
            audio = self[index]
            del self[index]
            return audio
            
    def index(self, audio):
        for i, a in enumerate(self._audio_list):
            if audio == a:
                return i
        raise Exception # FIXME: make more specific later
        
    def count(self, audio):
        count = 0
        for a in self.audio_list:
            if audio == a: 
                count += 1
        return count
            
    # FIXME: do this correctly
    def reverse(self):
        self._audio_list = self._audio_list[::-1]
    
    def clear(self):
        self._audio_list = []
        self.reset() 

    def duration(self):
        duration = 0
        for audio in self:
            if audio.length > 0:
                duration += audio.length
        return duration

    def _order_by_album(self):
        """ Assumes a pre-sorted list by artist """
        i = 0
        artist = self[i].artist
        for j in range(len(self)):
            if self[j].artist != artist:
                quicksort(self, i, j-1, 'album')
                i = j
                artist = self[i].artist
        quicksort(self, i, j-1, 'album')

    def _order_by_track(self):
        """ Assumes a pre-sorted list by album """
        i = 0
        album = self[i].album
        for j in range(len(self)):
            if self[j].album != album:
                quicksort(self, i, j-1, 'track')
                i = j
                album = self[i].album
        quicksort(self, i, j-1, 'track')

    def sort(self, by='artist'):
        quicksort(self, 0, len(self)-1, by)
        if by == 'artist':
            self._order_by_album()
        if by == 'album' or by == 'artist':
            self._order_by_track()

    def all_audio(self, with_shuffle=True):
        """ Returns all Audio objects in the playlist, optionally in shuffle
            order. with_shuffle only has effect if already shuffling """
        if with_shuffle and self.is_shuffling():
            return [self._audio_list[i] for i in self._order]
        return self._audio_list

    def set_shuffle(self, shuffle):
        self._shuffle = shuffle
        self._reorder()
        
    def is_shuffling(self):
        return self._shuffle

    def set_repeat(self, setting):
        self._repeat = setting

    def get_repeat(self):
        return self._repeat
        
    def is_repeating(self):
        return self.is_repeating_one() or self.is_repeating_all()
        
    def is_repeating_one(self):
        return self._repeat == REPEAT_ONE

    def is_repeating_all(self):
        return self._repeat == REPEAT_ALL
        
    def peek_next(self):
        """ Returns the next Audio object in the list after the current """
        if self.is_repeating_one():
            return self._audio_list[self._order[self.current_index]]
        elif self.is_repeating_all():
            if self.current_index+1 == len(self):
                return self._audio_list[self._order[0]]
            return self._audio_list[self._order[self.current_index+1]]
        elif not self.is_repeating():
            if self.current_index+1 == len(self):
                return None
            return self._audio_list[self._order[self.current_index+1]]

    # FIXME: this doesn't account for the case where it's set to repeat one
    #        song (and it has at least once). Is this an issue?
    def peek_previous(self):
        if self.current_index == 0:
            return self._audio_list[self._order[len(self._order)-1]]
        return self._audio_list[self._order[self.current_index-1]]

    def next(self):
        """ Gets the next Audio object in the list and makes it the current """
        audio = self.peek_next()
        if self.is_repeating_all():
            if self.current_index+1 == len(self):
                self.current_index = 0
            else:
                self.current_index += 1
        elif not self.is_repeating():
            if self.current_index+1 == len(self):
                self.current_index = 0
            else:
                self.current_index += 1
        return audio

    # FIXME: this, too, ignores the case where a single song is repeating
    def previous(self):
        audio = self.peek_previous()
        if self.current_index == 0:
            self.current_index = len(self) - 1
        else:
            self.current_index -= 1
        return audio
        
    # exports the Playlist object to a playlist file (.m3u, .pls, etc.)
    def export(self, type, uri):
        encoder = get_encoder(type)
        encoder.encode(self, uri)

    # Playlists are considered unique by name only
    def __eq__(self, playlist):
        return (self.name == playlist.name)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name
        
    def __repr__(self):
        id = ""
        if hasattr(self, 'id'):
            id = str(self.id)
        return u"<Playlist('%s', '%s')>" % (id, self.name)


def quicksort(audio_list, left, right, by):
    if right > left:
        pivot = (left+right)/2
        new_pivot = partition(audio_list, left, right, pivot, by)
        quicksort(audio_list, left, new_pivot-1)
        quicksort(audio_list, new_pivot+1, right)

def partition(audio_list, left, right, pivot, by):
    pivot_val = audio_list[pivot]
    audio_list[pivot], audio_list[right] = audio_list[right], audio_list[pivot]
    index = left
    for i in range(left, right):
        if audio_list[i].lt(pivot_val, by):
            audio_list[i], audio_list[index] = audio_list[index], audio_list[i]
            index += 1
    audio_list[index], audio_list[right] = audio_list[right], audio_list[index]
    return index
