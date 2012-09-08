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

import re
import os

class EventGenerator(object):
    def __init__(self):
        self.events = {}

    def connect(self, event, callback):
        if event not in self.events:
            self.events[event] = Event()
        self.events[event].add_listener(callback)

    def disconnect(self, event, callback):
        if event not in self.events:
            return
        self.events[event].remove_listener(callback)
        
    def emit(self, event, *args, **kwargs):
        if event not in self.events:
            return
        self.events[event](*args, **kwargs)

class Event(object):
    def __init__(self):
        self.listeners = set()

    def add_listener(self, listener):
        self.listeners.add(listener)
        return self

    def remove_listener(self, listener):
        self.listeners.pop(listener)
        return self

    def __call__(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)

ext_regex = re.compile(r"^.+\.(.+)$")
def get_extension(uri):
    if uri.find(os.sep):
        uri = os.path.split(uri)[1]
    match = ext_regex.match(uri)
    if match is not None:
        return match.group(1)
    raise ValueError("No extension found")
