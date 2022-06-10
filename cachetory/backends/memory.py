from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Generic, Optional

from cachetory.interfaces.backend import TV, SyncBackendRead, SyncBackendWrite


class MemoryBackend(SyncBackendRead[TV], SyncBackendWrite[TV]):
    __slots__ = ("_entries",)

    def __init__(self):
        self._entries: Dict[str, _Entry[TV]] = {}

    def _get_entry(self, key: str) -> _Entry[TV]:
        entry = self._entries[key]
        if entry.deadline is not None and entry.deadline > datetime.now(timezone.utc):
            self._entries.pop(key, None)  # might get popped by another thread
            raise KeyError(f"`{key}` has expired")
        return entry

    def __getitem__(self, key: str) -> TV:
        return self._get_entry(key).value

    def expire_at(self, key: str, deadline: Optional[datetime]) -> None:
        try:
            entry = self._get_entry(key)
        except KeyError:
            pass
        else:
            entry.deadline = deadline

    def set(self, key: str, value: TV, time_to_live: Optional[timedelta] = None) -> None:
        deadline = datetime.now(timezone.utc) + time_to_live if time_to_live is not None else None
        self._entries[key] = _Entry[TV](value, deadline)

    def delete(self, key: str) -> bool:
        return self._entries.pop(key, _SENTINEL) is _SENTINEL

    def __delitem__(self, key: str) -> None:
        del self._entries[key]


class _Entry(Generic[TV]):
    """
    `mypy` doesn't support generic named tuples, thus defining this little one.
    """

    value: TV
    deadline: Optional[datetime]

    __slots__ = ("value", "deadline")

    def __init__(self, value: TV, deadline: Optional[datetime]):
        self.value = value
        self.deadline = deadline


_SENTINEL = object()
