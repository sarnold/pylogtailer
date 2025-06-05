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


def callback(filename, lines):
    print(filename, lines)


def test_log_watcher(tmp_path, capfd):
    """
    Create and read a short log file
    """
    tf1 = tmp_path / "tftpd.log"
    tf1.write_text(log_str, encoding="utf-8")
    lw = LogWatcher(str(tmp_path), callback)
    lw.loop(blocking=False)
    out, err = capfd.readouterr()
    print(out)
