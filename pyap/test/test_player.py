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

from pyap.audio import Audio
from pyap.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_play(self):
        self.player.play(Audio('http://mp1.somafm.com:2020'))
        self.assertTrue(self.player.is_streaming())

    def test_play_uri(self):
        self.player.play_uri('http://mp1.somafm.com:2020', True)
        self.assertTrue(self.player.is_streaming())

    def test_pause(self):
        self.player.play(Audio('http://mp1.somafm.com:2020'))
        self.player.pause()
        self.assertTrue(self.player.is_paused())

    def test_resume(self):
        self.player.play(Audio('http://mp1.somafm.com:2020'))
        self.player.pause()
        self.assertTrue(self.player.is_paused())

    def test_stop(self):
        self.player.play(Audio('http://mp1.somafm.com:2020'))
        self.player.stop()
        self.assertTrue(self.player.is_stopped())

    def test_set_position(self):
        pass

    def test_get_position(self):
        pass

    def test_get_duration(self):
        pass

    def test_get_progress(self):
        pass

    def test_set_volume(self):
        self.player.play(Audio('http://mp1.somafm.com:2020'))
        self.player.set_volume(10)
        self.assertEqual(self.player.get_volume(), 10)

    def test_get_volume(self):
        self.player.play(Audio('http://mp1.somafm.com:2020'))
        self.player.set_volume(10)
        self.assertEqual(self.player.get_volume(), 10)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPlayer))
    return suite

if __name__ == '__main__':
    unittest.main()
