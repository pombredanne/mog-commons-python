# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import six
from mog_commons import string, unittest


class TestString(unittest.TestCase):
    def test_unicode_width(self):
        self.assertEqual(string.unicode_width(b'abc'), 3)
        self.assertEqual(string.unicode_width('あいう'.encode('utf-8')), 9)
        self.assertEqual(string.unicode_width('あいう'), 6)

    def test_to_str(self):
        self.assertEqual(string.to_str(b'abc'), string.to_str('abc'))
        self.assertEqual(string.to_str(1.23), '1.23')

    @unittest.base_unittest.skipUnless(six.PY2, 'requires Python 2')
    def test_to_str_py2(self):
        s = 'あいう'
        t = s.encode('utf-8')
        self.assertTrue(isinstance(s, unicode))
        self.assertTrue(isinstance(string.to_str(s), str))
        self.assertTrue(isinstance(t, str))
        self.assertTrue(isinstance(string.to_str(t), str))
        self.assertEqual(string.to_str(s), string.to_str(t))

    @unittest.base_unittest.skipUnless(six.PY3, 'requires Python 3')
    def test_to_str_py3(self):
        s = 'あいう'
        t = s.encode('utf-8')
        self.assertTrue(isinstance(s, str))
        self.assertTrue(isinstance(string.to_str(s), str))
        self.assertTrue(isinstance(t, bytes))
        self.assertTrue(isinstance(string.to_str(t), str))
        self.assertEqual(string.to_str(s), string.to_str(t))

    def test_to_unicode(self):
        self.assertEqual(string.to_unicode(b'abc'), 'abc')
        self.assertEqual(string.to_unicode('あいう'), 'あいう')
        self.assertEqual(string.to_unicode(1.23), '1.23')

    def test_to_bytes(self):
        self.assertEqual(string.to_bytes(b'abc'), b'abc')
        self.assertEqual(string.to_bytes('あいう'), 'あいう'.encode('utf-8'))
        self.assertEqual(string.to_bytes(1.23), b'1.23')

    def test_edge_just(self):
        self.assertEqual(string.edge_just('', '', 0), ' ')
        self.assertEqual(string.edge_just('', '', -1), ' ')
        self.assertEqual(string.edge_just('', '', 10), '          ')
        self.assertEqual(string.edge_just('', 'abcde', 10), '     abcde')
        self.assertEqual(string.edge_just('abc', 'de', 10), 'abc     de')
        self.assertEqual(string.edge_just('abcde', 'fghij', 10), 'abcde fghij')

    def test_edge_just_unicode(self):
        self.assertEqual(string.edge_just('', '', 0), ' ')
        self.assertEqual(string.edge_just('', '', -1), ' ')
        self.assertEqual(string.edge_just('', '', 10), '          ')
        self.assertEqual(string.edge_just('', 'あいう', 10), '    あいう')
        self.assertEqual(string.edge_just('あいu', 'えo', 10), 'あいu  えo')
        self.assertEqual(string.edge_just('あいう', 'えお', 10), 'あいう えお')

    def test_unicode_left(self):
        self.assertEqual(string.unicode_left('', 3), '')
        self.assertEqual(string.unicode_left('abcde', 3), 'abc')
        self.assertEqual(string.unicode_left('abcde', -3), '')
        self.assertEqual(string.unicode_left('あいうえお', 0), '')
        self.assertEqual(string.unicode_left('あいうえお', 1), '')
        self.assertEqual(string.unicode_left('あいうえお', 2), 'あ')
        self.assertEqual(string.unicode_left('あいうえお', 3), 'あ')
        self.assertEqual(string.unicode_left('あいうえお', 4), 'あい')
        self.assertEqual(string.unicode_left('あいうえお', 5), 'あい')
        self.assertEqual(string.unicode_left('あいうえお', 9), 'あいうえ')
        self.assertEqual(string.unicode_left('あいうえお', 10), 'あいうえお')
        self.assertEqual(string.unicode_left('あいうえお', 11), 'あいうえお')
        self.assertEqual(string.unicode_left('あxいxうxえxお', 4), 'あx')
        self.assertEqual(string.unicode_left('あxいxうxえxお', 5), 'あxい')

    def test_unicode_right(self):
        self.assertEqual(string.unicode_right('', 3), '')
        self.assertEqual(string.unicode_right('abcde', 3), 'cde')
        self.assertEqual(string.unicode_right('abcde', -3), '')
        self.assertEqual(string.unicode_right('あいうえお', 0), '')
        self.assertEqual(string.unicode_right('あいうえお', 1), '')
        self.assertEqual(string.unicode_right('あいうえお', 2), 'お')
        self.assertEqual(string.unicode_right('あいうえお', 3), 'お')
        self.assertEqual(string.unicode_right('あいうえお', 4), 'えお')
        self.assertEqual(string.unicode_right('あいうえお', 5), 'えお')
        self.assertEqual(string.unicode_right('あいうえお', 9), 'いうえお')
        self.assertEqual(string.unicode_right('あいうえお', 10), 'あいうえお')
        self.assertEqual(string.unicode_right('あいうえお', 11), 'あいうえお')
        self.assertEqual(string.unicode_right('あxいxうxえxお', 4), 'xお')
        self.assertEqual(string.unicode_right('あxいxうxえxお', 5), 'えxお')
