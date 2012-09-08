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

# Audio extensions
ASF = set(["asf", "wma"])
FLAC = set(["flac"])
AAC = set(["mp4", "m4a", "aac"])
MONKEYSAUDIO = set(["ape"])
MP3 = set(["mp3"])
MUSEPACK = set(["mpc", "mp+", "mpp"])
OGG = set(["ogg", "oga"])
TRUEAUDIO = set(["tta"])
WAVPACK = set(["wv"])
OPTIMFROG = set(["ofr"])

# Playlist extensions
M3U = set(["m3u"])
PLS = set(["pls"])

AUDIO = set()
AUDIO |= ASF | FLAC | AAC | MONKEYSAUDIO | MP3 | MUSEPACK | OGG | \
         TRUEAUDIO | WAVPACK | OPTIMFROG

PLAYLIST = set()
PLAYLIST |= M3U | PLS

def get_format(ext):
    if ext in ASF:
        return "asf"
    elif ext in FLAC:
        return "flac"
    elif ext in AAC:
        return "aac"
    elif ext in MONKEYSAUDIO:
        return "monkeysaudio"
    elif ext in MP3:
        return "mp3"
    elif ext in MUSEPACK:
        return "musepack"
    elif ext in OGG:
        return "ogg"
    elif ext in TRUEAUDIO:
        return "trueaudio"
    elif ext in WAVPACK:
        return "wavpack"
    elif ext in OPTIMFROG:
        return "optimfrog"
    elif ext in M3U:
        return "m3u"
    elif ext in PLS:
        return "pls"
    elif ext in AUDIO:
        return "audio"
    elif ext in PLAYLIST:
        return "playlist"
    return "unknown"
