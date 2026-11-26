from __future__ import annotations

import sys

import pytest

from exo.utils.async_process import AsyncProcess


@pytest.mark.skipif(sys.platform != "win32", reason="Windows runner transport guard")
@pytest.mark.asyncio
async def test_windows_runner_start_fails_with_a_clear_platform_error() -> None:
    with pytest.raises(RuntimeError, match="runner subprocess I/O is not supported"):
        await AsyncProcess().run()
