"""Hash Map implementation using open addressing with linear probing."""

from enum import Enum
from typing import Optional, Iterator, Tuple, List


DEFAULT_CAPACITY = 16
MAX_LOAD_FACTOR = 0.75


class EntryState(Enum):
    """State of an entry in the hash map."""

    EMPTY = 0
    TOMBSTONE = 1
    OCCUPIED = 2


class Entry:
    """A single entry in the hash map."""

    __slots__ = ("state", "key", "value")

    def __init__(self) -> None:
        self.state: EntryState = EntryState.EMPTY
        self.key: str = ""
        self.value: str = ""


class HashMap:
    """Hash map implementation using open addressing with linear probing.

    Provides O(1) average-case complexity for insert, get, and remove operations.
    """

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        """Create a new HashMap with the specified capacity."""
        capacity = max(capacity, DEFAULT_CAPACITY)
        self._entries: List[Entry] = [Entry() for _ in range(capacity)]
        self._size: int = 0
        self._tombstones: int = 0

    def __len__(self) -> int:
        """Return the number of elements in the map."""
        return self._size

    def __bool__(self) -> bool:
        """Return True if the map is not empty."""
        return self._size > 0

    @property
    def capacity(self) -> int:
        """Return the current capacity of the map."""
        return len(self._entries)

    def _load_factor(self) -> float:
        """Calculate the current load factor."""
        return (self._size + self._tombstones) / len(self._entries)

    def _hash_key(self, key: str) -> int:
        """Compute hash for a key."""
        return hash(key)

    def _find_slot(self, key: str) -> Tuple[int, bool]:
        """Find the slot for a key.

        Returns:
            Tuple of (index, found) where found indicates if the key exists.
        """
        h = self._hash_key(key)
        capacity = len(self._entries)
        index = h % capacity
        first_tombstone: Optional[int] = None

        for _ in range(capacity):
            entry = self._entries[index]

            if entry.state == EntryState.EMPTY:
                return (
                    first_tombstone if first_tombstone is not None else index,
                    False,
                )
            elif entry.state == EntryState.TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = index
            elif entry.state == EntryState.OCCUPIED:
                if entry.key == key:
                    return (index, True)

            index = (index + 1) % capacity

        return (first_tombstone if first_tombstone is not None else 0, False)

    def _resize(self) -> None:
        """Resize the hash map to double its capacity."""
        new_capacity = len(self._entries) * 2
        old_entries = self._entries

        self._entries = [Entry() for _ in range(new_capacity)]
        self._size = 0
        self._tombstones = 0

        for entry in old_entries:
            if entry.state == EntryState.OCCUPIED:
                self.insert(entry.key, entry.value)

    def insert(self, key: str, value: str) -> Optional[str]:
        """Insert a key-value pair into the map.

        Args:
            key: The key to insert.
            value: The value to associate with the key.

        Returns:
            The previous value if the key existed, None otherwise.
        """
        if self._load_factor() >= MAX_LOAD_FACTOR:
            self._resize()

        index, found = self._find_slot(key)

        if found:
            old_value = self._entries[index].value
            self._entries[index].value = value
            return old_value

        entry = self._entries[index]
        if entry.state == EntryState.TOMBSTONE:
            self._tombstones -= 1

        entry.state = EntryState.OCCUPIED
        entry.key = key
        entry.value = value
        self._size += 1
        return None

    def get(self, key: str) -> Optional[str]:
        """Get the value associated with a key.

        Args:
            key: The key to look up.

        Returns:
            The value if found, None otherwise.
        """
        index, found = self._find_slot(key)
        if found:
            return self._entries[index].value
        return None

    def remove(self, key: str) -> Optional[str]:
        """Remove a key-value pair from the map.

        Args:
            key: The key to remove.

        Returns:
            The removed value if the key existed, None otherwise.
        """
        index, found = self._find_slot(key)
        if found:
            entry = self._entries[index]
            old_value = entry.value
            entry.state = EntryState.TOMBSTONE
            entry.key = ""
            entry.value = ""
            self._size -= 1
            self._tombstones += 1
            return old_value
        return None

    def contains(self, key: str) -> bool:
        """Check if the map contains the given key.

        Args:
            key: The key to check.

        Returns:
            True if the key exists, False otherwise.
        """
        _, found = self._find_slot(key)
        return found

    def clear(self) -> None:
        """Remove all entries from the map."""
        for entry in self._entries:
            entry.state = EntryState.EMPTY
            entry.key = ""
            entry.value = ""
        self._size = 0
        self._tombstones = 0

    def keys(self) -> Iterator[str]:
        """Iterate over all keys in the map."""
        for entry in self._entries:
            if entry.state == EntryState.OCCUPIED:
                yield entry.key

    def values(self) -> Iterator[str]:
        """Iterate over all values in the map."""
        for entry in self._entries:
            if entry.state == EntryState.OCCUPIED:
                yield entry.value

    def items(self) -> Iterator[Tuple[str, str]]:
        """Iterate over all key-value pairs in the map."""
        for entry in self._entries:
            if entry.state == EntryState.OCCUPIED:
                yield (entry.key, entry.value)

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator."""
        return self.contains(key)

    def __getitem__(self, key: str) -> str:
        """Support bracket notation for getting values."""
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key: str, value: str) -> None:
        """Support bracket notation for setting values."""
        self.insert(key, value)

    def __delitem__(self, key: str) -> None:
        """Support del operator."""
        if self.remove(key) is None:
            raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        """Iterate over keys."""
        return self.keys()
