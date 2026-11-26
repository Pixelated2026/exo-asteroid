from __future__ import annotations


def ensure_nofile_limit(minimum: int) -> None:
    """Raise the POSIX open-file soft limit where the platform supports it.

    Windows has no RLIMIT_NOFILE equivalent; socket and handle limits are managed
    by the operating system, so this is intentionally a no-op there.
    """
    try:
        import resource
    except ImportError:
        return

    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    target = min(max(soft, minimum), hard)
    resource.setrlimit(resource.RLIMIT_NOFILE, (target, hard))
