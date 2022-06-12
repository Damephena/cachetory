from datetime import timedelta
from functools import wraps
from typing import Callable, Optional, Union

from typing_extensions import Concatenate, ParamSpec

from cachetory.caches.sync import Cache
from cachetory.decorators.private import make_key_by_default
from cachetory.interfaces.serializers import ValueT

P = ParamSpec("P")  # original function parameter specs


def cached(
    cache: Union[Cache, Callable[P, Cache[ValueT]]],
    *,
    make_key: Callable[Concatenate[Callable[P, ValueT], P], str] = make_key_by_default,
    time_to_live: Optional[timedelta] = None,
    if_not_exists: bool = False,
):
    """
    Args:
        cache: `Cache` instance or a callable tha returns a `Cache` instance for each function call.
        make_key: callable to generate a custom cache key per each call.
        if_not_exists: controls concurrent sets: if `True` – avoids overwriting a cached value.
        time_to_live: cached value expiration time.
    """

    def wrap(callable_: Callable[P, ValueT]) -> Callable[P, ValueT]:
        @wraps(callable_)
        def cached_callable(*args, **kwargs) -> ValueT:
            cache_ = cache() if callable(cache) else cache
            key_ = make_key(callable_, *args, **kwargs)
            try:
                value = cache_[key_]
            except KeyError:
                value = callable_(*args, **kwargs)
                cache_.set(key_, value, time_to_live=time_to_live, if_not_exists=if_not_exists)
            return value

        return cached_callable

    return wrap
