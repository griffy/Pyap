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
from pyap.audio import *
from pyap.player import Player

class TestAudio(unittest.TestCase):
    """
    A test class for the Audio module
    """
    def setUp(self):
        self.audio = Audio(os.path.join('resources', 'test.mp3'))

    def test_uri_type(self):
        uris = [
            'http://mp1.somafm.com:2020',
            os.path.join('resources', 'test.mp3'),
            os.path.abspath(os.path.join('resources', 'test.mp3')),
            os.path.join('resources', 'test.music'),
            os.path.join('resources', 'test')
        ]
        expected_types = [
            STREAM,
            FILE,
            FILE,
            UNKNOWN,
            UNKNOWN
        ]
        for i, uri in enumerate(uris):
            self.assertEqual(uri_type(uri), expected_types[i])

    def test_audio_info(self):
        uris = [
            os.path.abspath(os.path.join('resources', 'test')),
            os.path.abspath(os.path.join('resources', 'test.mp3'))
        ]
        expected_infos = [
            None, 
            {
                'length': 1,
                'track': 1,
                'year': u'2005',
                'artist': u'Artist',
                'title': u'Title',
                'album': u'Album'
            }
        ]
        for i, uri in enumerate(uris):
            self.assertEqual(audio_info(uri), expected_infos[i])

    def test_init(self):
        uris = [
            os.path.join('resources', 'test.mp3'),
            os.path.abspath(os.path.join('resources', 'test.mp3'))
        ]
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

    def test_play(self):
        def callback(audio):
            self.audio_finished = True
        self.audio_finished = False
        self.audio.play(on_finish=callback)
        while not self.audio_finished: pass
        self.assertTrue(self.audio_finished)
        player = Player()
        self.audio_finished = False
        self.audio.play(player, on_finish=callback)
        while not self.audio_finished: pass
        self.assertTrue(self.audio_finished)

    # TODO
    def test_pause(self): pass
    def test_resume(self): pass
    def test_stop(self): pass

    def test_is_playing(self):
        self.assertFalse(self.audio.is_playing())
        self.audio.play()
        self.assertTrue(self.audio.is_playing())
        self.audio.stop()

    def test_is_streaming(self):
        audio = Audio('http://mp1.somafm.com:2020')
        self.assertFalse(audio.is_streaming())
        audio.play()
        self.assertTrue(audio.is_streaming())
        audio.stop()

    def test_is_paused(self):
        self.assertFalse(self.audio.is_paused())
        self.audio.play()
        self.assertFalse(self.audio.is_paused())
        self.audio.pause()
        self.assertTrue(self.audio.is_paused())
        self.audio.stop()

    def test_is_stopped(self):
        self.assertTrue(self.audio.is_stopped())
        self.audio.play()
        self.assertFalse(self.audio.is_stopped())
        self.audio.stop()
        self.assertTrue(self.audio.is_stopped())

    def test_is_file(self):
        self.assertTrue(self.audio.is_file())

    def test_is_stream(self):
        self.assertFalse(self.audio.is_stream())

    def test___cmp__(self):
        # All Apologies to the Nirvana diehards who would like
        # for the title to read as "tourette's"
        audio1 = Audio(os.path.join('resources', 'test.mp3'),
            title="Tourette's"
        )
        audio2 = Audio(os.path.join('resources', 'test.mp3'),
            title="Lazy Eye"
        )

        audio3 = Audio(os.path.join('resources', 'test.mp3'),
            artist="Nirvana", title="Tourette's"
        )
        audio4 = Audio(os.path.join('resources', 'test.mp3'),
            artist="Silversun Pickups", title="Lazy Eye"
        )

        audio5 = Audio(os.path.join('resources', 'test.mp3'),
            artist="Nirvana", title="Tourette's"
        )
        audio6 = Audio(os.path.join('resources', 'test.mp3'),
            artist="Nirvana", title="Lounge Act"
        )

        audio7 = Audio(os.path.join('resources', 'test.mp3'),
            artist="Nirvana", album="In Utero", title="Tourette's"
        )
        audio8 = Audio(os.path.join('resources', 'test.mp3'),
            artist="Nirvana", album="Nevermind", title="Lounge Act"
        )

        audio9 = Audio(os.path.join('resources', 'test.mp3'),
            artist="Nirvana", album="In Utero", title="Tourette's"
        )
        audio10 = Audio(os.path.join('resources', 'test.mp3'),
            artist="Nirvana", album="In Utero", title="All Apologies"
        )

        audio11 = Audio(os.path.join('resources', 'test.mp3'),
            artist="Nirvana", album="In Utero", track="11", title="Tourette's"
        )
        audio12 = Audio(os.path.join('resources', 'test.mp3'),
            artist="Nirvana", album="In Utero", track="12", title="All Apologies"
        )

        self.assertTrue(audio1 > audio2)
        self.assertTrue(audio3 < audio4)
        self.assertTrue(audio5 > audio6)
        self.assertTrue(audio7 < audio8)
        self.assertTrue(audio9 > audio10)
        self.assertTrue(audio11 < audio12)

    def test___str__(self):
        self.assertEqual(self.audio.__str__(), "Artist - Title")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAudio))
    return suite

if __name__ == '__main__':
    unittest.main()
