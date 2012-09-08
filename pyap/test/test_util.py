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

from pyap.util import *

class TestUtil(unittest.TestCase):
    """
    A test class for the util module
    """

    def test_get_extension(self):
        uris = (r'file.mp3',
                r'file.name.mp3',
                r'/home/test/file.mp3',
                r'/home/test/file.name.mp3',
                r'C:\Users\test\file.mp3',
                r'C:\Users\test\file.name.mp3')
        for uri in uris:
            self.assertEqual(get_extension(uri), "mp3")

        uri = "file"
        self.assertRaises(ValueError, get_extension, uri)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUtil))
    return suite

if __name__ == '__main__':
    unittest.main()
