from urllib.parse import urlparse

from cachetory.interfaces.backends.async_ import AsyncBackend

from .dummy import DummyBackend
from .memory import MemoryBackend

try:
    # noinspection PyUnresolvedReferences
    from .redis import RedisBackend
except ImportError:
    _is_redis_available = False
else:
    _is_redis_available = True


async def from_url(url: str) -> AsyncBackend:
    """
    Creates an asynchronous backend from the given URL.

    Examples:
        >>> await from_url("redis://localhost:6379")
    """
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    if scheme == "memory":
        return await MemoryBackend.from_url(url)
    if scheme in ("redis", "rediss", "redis+unix"):
        if not _is_redis_available:
            raise ValueError(f"`{scheme}://` requires `cachetory[redis-async]` extra")
        return await RedisBackend.from_url(url)
    if scheme == "dummy":
        return await DummyBackend.from_url(url)
    raise ValueError(f"`{scheme}://` is not supported")
