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

import unittest

from pyap.audio import Audio

class TestAudio(unittest.TestCase):
    """
    A test class for the Audio module
    """
    def setUp(self):
        self.audio = Audio('/home/test/Pyap/test.mp3')

    def test_init(self):
        uris = ('test.mp3',
                '/home/test/Pyap/test.mp3')
        for uri in uris:
            audio = Audio(uri)
            self.assertEqual(audio.type, Audio.FILE)
            self.assertEqual(audio.artist, "Nirvana")
            self.assertEqual(audio.title, "All Apologies")
            self.assertEqual(audio.album, "In Utero")
            self.assertEqual(audio.uri, '/home/test/Pyap/test.mp3')

        uri = 'http://mp1.somafm.com:2020'
        audio = Audio(uri)
        self.assertEqual(audio.type, Audio.STREAM)

    def test_is_file(self):
        self.assertTrue(self.audio.is_file())

    def test_is_stream(self):
        self.assertFalse(self.audio.is_stream())

    def test_str(self):
        self.assertEqual(self.audio.__str__(), "Nirvana - All Apologies")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAudio))
    return suite

if __name__ == '__main__':
    unittest.main()
