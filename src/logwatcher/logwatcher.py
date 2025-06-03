"""
Real-time log file watcher supporting log rotation.
Works with Python >= 3.2, on both POSIX and Windows.
"""

import os
import time
import errno
import stat

from shlex import split
from typing import Callable, Dict


class LogWatcher:
    """
    """

    def __init__(self, folder: str, callback: Callable, extensions = "log",
                tail_lines: int = 0, sizehint: int = 1048576):
        """
        Looks for changes in all files of a directory. This is useful for
        watching log file changes in real-time. It also supports file rotation.

        Example:

        >>> def callback(filename, lines):
        ...     print(filename, lines)
        ...
        >>> lw = LogWatcher("/var/log/", callback)
        >>> lw.loop()

        (str) @folder:
            the folder to watch

        (callable) @callback:
            a function which is called every time one of the file being
            watched is updated;
            this is called with "filename" and "lines" arguments.

        (list) @extensions:
            only watch files with these extensions

        (int) @tail_lines:
            read last N lines from files being watched before starting

        (int) @sizehint: passed to file.readlines(), represents an
            approximation of the maximum number of bytes to read from
            a file on every ieration (as opposed to load the entire
            file in memory until EOF is reached). Defaults to 1MB.
        """
        self.folder = os.path.realpath(folder)
        self.extensions = split(extensions)
        self._files_map: Dict = {}
        self._callback = callback
        self._sizehint = sizehint
        assert os.path.isdir(self.folder), self.folder
        assert callable(callback), repr(callback)
        self.update_files()
        for _, file in self._files_map.items():
            file.seek(os.path.getsize(file.name))  # EOF
            if tail_lines:
                try:
                    lines = self.tail(file.name, tail_lines)
                except IOError as err:
                    if err.errno != errno.ENOENT:
                        raise
                else:
                    if lines:
                        self._callback(file.name, lines)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        self.close()

    def loop(self, interval=0.1, blocking=True):
        """
        Start a busy loop checking for file changes every *interval*
        seconds. If *blocking* is False make one loop then return.
        """
        # May be overridden in order to use pyinotify lib and block
        # until the directory being watched is updated.
        # Note that directly calling readlines() as we do is faster
        # than first checking file's last modification times.
        while True:
            self.update_files()
            for _, file in list(self._files_map.items()):
                self.readlines(file)
            if not blocking:
                return
            time.sleep(interval)

    def log(self, line):
        """Log when a file is un/watched"""
        print(line)

    def listdir(self):
        """List directory and filter files by extension.
        You may want to override this to add extra logic or globbing
        support.
        """
        ls = os.listdir(self.folder)
        if self.extensions:
            return [x for x in ls if os.path.splitext(x)[1][1:] \
                                           in self.extensions]
        return ls

    @classmethod
    def open(cls, file):
        """Wrapper around open().
        By default files are opened in binary mode and readlines()
        will return bytes on both Python 2 and 3.
        This means callback() will deal with a list of bytes.
        Can be overridden in order to deal with unicode strings
        instead, like this:

          import codecs, locale
          return codecs.open(file, 'r', encoding=locale.getpreferredencoding(),
                             errors='ignore')
        """
        return open(file, 'rb')

    @classmethod
    def tail(cls, fname, window):
        """Read last N lines from file fname."""
        if window <= 0:
            msg = f'invalid window value: {window}'
            raise ValueError(msg)
        with cls.open(fname) as f:
            buff_size = 1024
            # True if open() was overridden and file was opened in text
            # mode. In that case readlines() will return unicode strings
            # instead of bytes.
            encoded = getattr(f, 'encoding', False)
            end = '\n' if encoded else b'\n'
            data = '' if encoded else b''
            f.seek(0, os.SEEK_END)
            fsize = f.tell()
            block = -1
            Exit = False
            while not Exit:
                step = block * buff_size
                if abs(step) >= fsize:
                    f.seek(0)
                    newdata = f.read(buff_size - (abs(step) - fsize))
                    Exit = True
                else:
                    f.seek(step, os.SEEK_END)
                    newdata = f.read(buff_size)
                data = newdata + data
                if data.count(end) >= window:
                    break
                block -= 1
            return data.splitlines()[-window:]

    def update_files(self):
        """
        Update file list, check existence, look for new ones.
        """
        ls = []
        for name in self.listdir():
            absname = os.path.realpath(os.path.join(self.folder, name))
            try:
                st = os.stat(absname)
            except EnvironmentError as err:
                if err.errno != errno.ENOENT:
                    raise
            else:
                if not stat.S_ISREG(st.st_mode):
                    continue
                fid = self.get_file_id(st)
                ls.append((fid, absname))

        # check existent files
        for fid, file in list(self._files_map.items()):
            try:
                st = os.stat(file.name)
            except EnvironmentError as err:
                if err.errno == errno.ENOENT:
                    self.unwatch(file, fid)
                else:
                    raise
            else:
                if fid != self.get_file_id(st):
                    # same name but different file (rotation); reload it.
                    self.unwatch(file, fid)
                    self.watch(file.name)

        # add new ones
        for fid, fname in ls:
            if fid not in self._files_map:
                self.watch(fname)

    def readlines(self, file):
        """
        Read file lines since last access until EOF is reached and
        invoke callback.
        """
        while True:
            lines = file.readlines(self._sizehint)
            if not lines:
                break
            self._callback(file.name, lines)

    def watch(self, fname):
        """
        Watch the specified file.
        """
        try:
            file = self.open(fname)
            fid = self.get_file_id(os.stat(fname))
        except EnvironmentError as err:
            if err.errno != errno.ENOENT:
                raise
        else:
            self.log(f"watching logfile {fname}")
            self._files_map[fid] = file

    def unwatch(self, file, fid):
        """
        File no longer exists. If it has been renamed try to read it
        for the last time in case we're dealing with a rotating log
        file.
        """
        self.log(f"un-watching logfile {file.name}")
        del self._files_map[fid]
        with file:
            lines = file.readlines(self._sizehint)
            if lines:
                self._callback(file.name, lines)

    @staticmethod
    def get_file_id(st):
        if os.name == 'posix':
            return f"{st.st_dev:x}g{st.st_ino:x}"
        return f"{st.st_ctime:f}"

    def close(self):
        """
        Close all ``_files_map`` items.
        """
        for _, file in self._files_map.items():
            file.close()
        self._files_map.clear()
