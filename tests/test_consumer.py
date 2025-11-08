import codecs
import locale
from pathlib import Path

import pytest

from logwatcher.logwatcher import LogWatcher

log_str = """
2025-04-20 19:32:12 UTC INFO tftpd.daemonize(149) Started
2025-04-20 19:32:12 UTC INFO tftpd.listen(95) Server requested on ip 0.0.0.0, port 9069
2025-04-20 19:32:12 UTC INFO tftpd.listen(107) Starting receive loop...
2025-04-20 19:32:24 UTC INFO tftpd.stop(262) Stopped
2025-04-20 19:42:43 UTC INFO tftpd.daemonize(149) Started
2025-04-20 19:42:43 UTC INFO tftpd.listen(95) Server requested on ip 0.0.0.0, port 9069
2025-04-20 19:42:43 UTC INFO tftpd.listen(107) Starting receive loop...
2025-04-20 19:42:56 UTC INFO tftpd.stop(262) Stopped
2025-05-05 02:41:07 UTC INFO tftpd.daemonize(149) Started
2025-05-05 02:41:07 UTC INFO tftpd.listen(95) Server requested on ip 0.0.0.0, port 9069
2025-05-05 02:41:07 UTC INFO tftpd.listen(107) Starting receive loop...
2025-05-05 02:41:11 UTC INFO tftpd.is_running(308) Process (pid 16011) is running...
2025-05-05 02:41:14 UTC INFO tftpd.stop(262) Stopped
2025-05-16 18:06:00 UTC INFO tftpd.daemonize(149) Started
2025-05-16 18:06:00 UTC INFO tftpd.listen(95) Server requested on ip 0.0.0.0, port 9069
2025-05-16 18:06:00 UTC INFO tftpd.listen(107) Starting receive loop...
2025-05-16 18:06:06 UTC INFO tftpd.stop(262) Stopped
"""


class TLogWatcher(LogWatcher):
    """Override ``open()`` to decode log lines"""

    @classmethod
    def open(cls, file):
        return codecs.open(file, 'r', encoding="utf-8", errors='ignore')


def loop_callback(filename, lines):
    print(filename, lines)


def test_log_watcher_loop(tmp_path):
    """
    Create and read a short log file
    """
    tf1 = tmp_path / "tftpd.log"
    tf1.write_text(log_str, encoding="utf-8")
    lw = LogWatcher(str(tmp_path), loop_callback)
    lw.loop(blocking=False)


def test_log_watcher_tail(tmp_path):
    """
    Create and read a short log file
    """
    tf1 = tmp_path / "tftpd.log"
    tf1.write_text(log_str, encoding="utf-8")
    lw = TLogWatcher(str(tmp_path), loop_callback)
    lines = lw.tail(str(tf1), 5)
    for line in lines:
        assert isinstance(line, str)
    print(f'\n{lines}')


def test_log_watcher_tail_lines(tmp_path, capfd):
    """
    Create and read a short log file
    """
    tf1 = tmp_path / "tftpd.log"
    tf1.write_text(log_str, encoding="utf-8")
    lw = TLogWatcher(str(tmp_path), loop_callback, tail_lines=2)
    lw.loop(blocking=False)
    out, err = capfd.readouterr()
    assert "tftpd.log" in out
    print(out)
