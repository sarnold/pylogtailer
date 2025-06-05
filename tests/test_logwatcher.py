# https://code.activestate.com/recipes/577968-log-watcher-tail-f-log

import atexit
import os
import sys
import unittest

from logwatcher.logwatcher import LogWatcher

TESTFN = '$testfile.log'
TESTFN2 = '$testfile2.log'


def b(s):
    return s.encode("utf-8")


class TestLogWatcher(unittest.TestCase):

    def setUp(self):
        def callback(filename, lines):
            self.filename.append(filename)
            for line in lines:
                self.lines.append(line)

        self.filename = []
        self.lines = []
        self.file = open(TESTFN, 'w')
        self.watcher = LogWatcher(os.getcwd(), callback)

    def tearDown(self):
        self.watcher.close()
        self.remove_test_files()

    def write_file(self, data):
        self.file.write(data)
        self.file.flush()

    @staticmethod
    @atexit.register
    def remove_test_files():
        for x in [TESTFN, TESTFN2]:
            try:
                os.remove(x)
            except EnvironmentError:
                pass

    def test_no_lines(self):
        self.watcher.loop(blocking=False)

    def test_one_line(self):
        self.write_file('foo')
        self.watcher.loop(blocking=False)
        self.assertEqual(self.lines, [b"foo"])
        self.assertEqual(self.filename, [os.path.abspath(TESTFN)])

    def test_two_lines(self):
        self.write_file('foo\n')
        self.write_file('bar\n')
        self.watcher.loop(blocking=False)
        self.assertEqual(
            self.lines,
            [b"foo\r\n", b"bar\r\n"] if sys.platform == "win32" else [b"foo\n", b"bar\n"],
        )
        self.assertEqual(self.filename, [os.path.abspath(TESTFN)])

    def test_new_file(self):
        with open(TESTFN2, "w") as f:
            f.write("foo")
        self.watcher.loop(blocking=False)
        self.assertEqual(self.lines, [b"foo"])
        self.assertEqual(self.filename, [os.path.abspath(TESTFN2)])

    def test_file_removed(self):
        self.write_file("foo")
        try:
            os.remove(TESTFN)
        except EnvironmentError:  # necessary on Windows
            pass
        self.watcher.loop(blocking=False)
        self.assertEqual(self.lines, [b"foo"])

    def test_tail(self):
        MAX = 10000
        content = '\n'.join([str(x) for x in range(0, MAX)])
        self.write_file(content)
        # input < BUFSIZ (1 iteration)
        lines = self.watcher.tail(self.file.name, 100)
        self.assertEqual(len(lines), 100)
        self.assertEqual(lines, [b(str(x)) for x in range(MAX - 100, MAX)])
        # input > BUFSIZ (multiple iterations)
        lines = self.watcher.tail(self.file.name, 5000)
        self.assertEqual(len(lines), 5000)
        self.assertEqual(lines, [b(str(x)) for x in range(MAX - 5000, MAX)])
        # input > file's total lines
        lines = self.watcher.tail(self.file.name, MAX + 9999)
        self.assertEqual(len(lines), MAX)
        self.assertEqual(lines, [b(str(x)) for x in range(0, MAX)])
        #
        self.assertRaises(ValueError, self.watcher.tail, self.file.name, 0)
        LogWatcher.tail(self.file.name, 10)

    def test_ctx_manager(self):
        with self.watcher:
            pass
