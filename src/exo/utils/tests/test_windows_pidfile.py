from __future__ import annotations

import sys

import pytest

from exo_rs import Pidfile


@pytest.mark.skipif(sys.platform != "win32", reason="Windows PID lock implementation only")
def test_windows_pidfile_uses_persistent_sidecar_lock(tmp_path) -> None:
    path = tmp_path / "exo.pid"
    lock_path = tmp_path / "exo.pid.lock"

    handle = Pidfile(path, 0o0600)
    handle.write()
    assert path.read_text(encoding="utf-8") == str(__import__("os").getpid())
    assert lock_path.exists()

    handle.close()
    assert not path.exists()
    assert lock_path.exists()

    next_handle = Pidfile(path, 0o0600)
    next_handle.write()
    next_handle.close()
