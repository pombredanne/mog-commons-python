# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import time
import six
from mog_commons.terminal import TerminalHandler
from mog_commons.unittest import TestCase, base_unittest, FakeBytesInput, FakeInput


class TestTerminal(TestCase):
    def test_clear(self):
        with self.withAssertOutput('', '') as (out, err):
            # assume this should not raise an error
            TerminalHandler(stdout=out, stderr=err).clear()

    def test_getch_from_file(self):
        with open(os.path.join('tests', 'resources', 'test_terminal_input.txt')) as f:
            t = TerminalHandler(stdin=f)
            self.assertEqual(t.getch(), 'a')
            self.assertRaises(EOFError, t.getch)

    @base_unittest.skipUnless(os.name != 'nt', 'requires POSIX compatible')
    def test_getch(self):
        self.assertEqual(TerminalHandler(stdin=FakeBytesInput(b'')).getch(), '')
        self.assertEqual(TerminalHandler(stdin=FakeBytesInput(b'\x03')).getch(), '\x03')
        self.assertEqual(TerminalHandler(stdin=FakeBytesInput(b'abc')).getch(), 'a')
        self.assertEqual(TerminalHandler(stdin=FakeBytesInput('あ'.encode('utf-8'))).getch(), '')
        self.assertEqual(TerminalHandler(stdin=FakeBytesInput('あ'.encode('sjis'))).getch(), '')

    def test_getch_disabled(self):
        t = TerminalHandler(stdin=FakeInput('a\nb\ncd\ne\n'), keep_input_clean=False, getch_enabled=False)
        self.assertEqual(t.getch(), 'a')
        self.assertEqual(t.getch(), 'b')
        self.assertEqual(t.getch(), 'c')
        self.assertEqual(t.getch(), 'e')
        self.assertRaises(EOFError, t.getch)

    @base_unittest.skipUnless(os.name != 'nt', 'requires POSIX compatible')
    def test_getch_key_repeat(self):
        fin = FakeBytesInput(b'abcde')

        def append_char(ch):
            fin.write(ch)
            fin.seek(-len(ch), 1)

        t1 = TerminalHandler(stdin=fin)
        self.assertEqual(t1.getch(), 'a')
        append_char(b'x')
        self.assertEqual(t1.getch(), 'x')
        append_char(b'x')
        self.assertEqual(t1.getch(), '')
        append_char(b'x')
        self.assertEqual(t1.getch(), '')
        append_char(b'y')
        self.assertEqual(t1.getch(), 'y')
        append_char(b'y')
        self.assertEqual(t1.getch(), '')

        time.sleep(1)
        append_char(b'y')
        self.assertEqual(t1.getch(), 'y')

    @base_unittest.skipUnless(os.name != 'nt', 'requires POSIX compatible')
    def test_getch_key_repeat_disabled(self):
        fin = FakeBytesInput(b'abcde')

        def append_char(ch):
            fin.write(ch)
            fin.seek(-len(ch), 1)

        t1 = TerminalHandler(stdin=fin, getch_repeat_threshold=0)
        self.assertEqual(t1.getch(), 'a')
        append_char(b'x')
        self.assertEqual(t1.getch(), 'x')
        append_char(b'x')
        self.assertEqual(t1.getch(), 'x')
        append_char(b'x')
        self.assertEqual(t1.getch(), 'x')
        append_char(b'y')
        self.assertEqual(t1.getch(), 'y')
        append_char(b'y')
        self.assertEqual(t1.getch(), 'y')

        time.sleep(1)
        append_char(b'y')
        self.assertEqual(t1.getch(), 'y')

    @base_unittest.skipUnless(os.name != 'nt', 'requires POSIX compatible')
    def test_getch_not_keep_input_clean(self):
        fin = FakeBytesInput(b'abcde')
        t1 = TerminalHandler(stdin=fin, keep_input_clean=False)
        self.assertEqual(t1.getch(), 'a')
        self.assertEqual(t1.getch(), 'b')
        self.assertEqual(t1.getch(), 'c')
        self.assertEqual(t1.getch(), 'd')
        self.assertEqual(t1.getch(), 'e')
        self.assertEqual(t1.getch(), '')

    def test_resolve_encoding(self):
        import io
        import codecs

        if six.PY2:
            out = codecs.getwriter('sjis')
            out.encoding = 'sjis'
        else:
            out = io.TextIOWrapper(six.StringIO(), 'sjis')

        self.assertEqual(TerminalHandler._detect_encoding(out), 'sjis')

    def test_init(self):
        self.assertEqual(TerminalHandler(stdin=six.StringIO(), getch_enabled=False).getch_enabled, False)
        self.assertEqual(TerminalHandler(stdin=six.StringIO(), getch_enabled=True).getch_enabled, False)
        self.assertEqual(TerminalHandler(stdin=FakeInput(), getch_enabled=False).getch_enabled, False)
        self.assertEqual(TerminalHandler(stdin=FakeInput(), getch_enabled=True).getch_enabled, True)
