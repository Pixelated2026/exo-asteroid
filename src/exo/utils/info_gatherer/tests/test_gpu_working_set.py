import json

import psutil
import pytest

from exo.shared.types.memory import Memory
from exo.utils.info_gatherer.macmon import MacmonMetrics
from exo.utils.info_gatherer.system_info import (
    _gpu_memory_from_device_info,
    get_gpu_working_set,
)

GB = 1024**3


def _macmon_line(ram_total: int, ram_usage: int) -> str:
    return json.dumps(
        {
            "timestamp": "2026-01-01T00:00:00Z",
            "temp": {"cpu_temp_avg": 40.0, "gpu_temp_avg": 35.0},
            "memory": {
                "ram_total": ram_total,
                "ram_usage": ram_usage,
                "swap_total": 0,
                "swap_usage": 0,
            },
            "ecpu_usage": [1000, 0.1],
            "pcpu_usage": [3000, 0.2],
            "gpu_usage": [1000, 0.0],
            "all_power": 10.0,
            "ane_power": 0.0,
            "cpu_power": 5.0,
            "gpu_power": 1.0,
            "gpu_ram_power": 0.0,
            "ram_power": 0.5,
            "sys_power": 12.0,
        }
    )


def test_memory_reports_carry_the_gpus_working_set() -> None:
    working_set = Memory.from_bytes(12_713_115_648)

    metrics = MacmonMetrics.from_raw_json(_macmon_line(16 * GB, 4 * GB), working_set)

    assert metrics.memory.ram_available == Memory.from_bytes(12 * GB)
    assert metrics.memory.gpu_working_set == working_set


def test_the_gpus_working_set_is_most_of_the_ram() -> None:
    working_set = get_gpu_working_set()
    if working_set is None:
        pytest.skip("Needs a Mac with Metal")

    ram = psutil.virtual_memory().total
    assert 0.5 * ram < working_set.in_bytes < ram



def test_cuda_device_info_reports_total_and_free_vram() -> None:
    total, available = _gpu_memory_from_device_info(
        {"total_memory": 12 * GB, "free_memory": 9 * GB}
    )

    assert total == Memory.from_bytes(12 * GB)
    assert available == Memory.from_bytes(9 * GB)


def test_cuda_device_info_accepts_memory_size_alias() -> None:
    total, available = _gpu_memory_from_device_info(
        {"memory_size": 24 * GB, "free_memory": 20 * GB}
    )

    assert total == Memory.from_bytes(24 * GB)
    assert available == Memory.from_bytes(20 * GB)


@pytest.mark.parametrize(
    "info",
    [
        {},
        {"total_memory": 12 * GB},
        {"total_memory": 0, "free_memory": 1},
        {"total_memory": 12 * GB, "free_memory": -1},
        {"total_memory": "12 GB", "free_memory": 1},
    ],
)
def test_invalid_cuda_device_info_is_ignored(info: dict[str, object]) -> None:
    assert _gpu_memory_from_device_info(info) is None
