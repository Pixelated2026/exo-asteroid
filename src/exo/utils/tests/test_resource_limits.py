from __future__ import annotations

import sys

from exo.utils.resource_limits import ensure_nofile_limit


def test_resource_limit_helper_is_a_noop_without_resource_module(
    monkeypatch,
) -> None:
    monkeypatch.setitem(sys.modules, "resource", None)
    ensure_nofile_limit(65535)
