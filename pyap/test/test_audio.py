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

import unittest
import os
import time
from pyap.audio import Audio

class TestAudio(unittest.TestCase):
    """
    A test class for the Audio module
    """
    def setUp(self):
        self.audio = Audio(os.path.join('resources', 'test.mp3'))

    def test_init(self):
        uris = (os.path.join('resources', 'test.mp3'),
                os.path.abspath(os.path.join('resources', 'test.mp3'))
        )
        for uri in uris:
            audio = Audio(uri)
            self.assertTrue(audio.is_file())
            self.assertEqual(audio.artist, "Artist")
            self.assertEqual(audio.title, "Title")
            self.assertEqual(audio.album, "Album")
            self.assertEqual(audio.uri, os.path.abspath(os.path.join('resources', 'test.mp3')))

        uri = 'http://mp1.somafm.com:2020'
        audio = Audio(uri)
        self.assertTrue(audio.is_stream())

    def test_is_file(self):
        self.assertTrue(self.audio.is_file())

    def test_is_stream(self):
        self.assertFalse(self.audio.is_stream())

    def test_play(self):
        self.audio_finished = False
        def callback(audio):
            self.audio_finished = True
        self.audio.play(on_finish=callback)
        while not self.audio_finished: pass
        self.assertTrue(self.audio_finished)

    def test_str(self):
        self.assertEqual(self.audio.__str__(), "Artist - Title")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAudio))
    return suite

if __name__ == '__main__':
    unittest.main()
