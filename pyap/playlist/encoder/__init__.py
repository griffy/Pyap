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

class Encoder(object):
    def encode(self, playlist):
        raise NotImplementedError("Encode is not implemented")

def get_encoder(encoder):
    if encoder == 'm3u':
        from pyap.playlist.encoder.m3u import M3UDecoder
        return M3UEncoder()
    elif encoder == 'pls':
        from pyap.playlist.encoder.pls import PLSDecoder
        return PLSEncoder()
