// Package hashmap provides a hash map implementation using open addressing with linear probing.
package hashmap

import (
	"github.com/cespare/xxhash/v2"
)

const (
	defaultCapacity = 16
	maxLoadFactor   = 0.75
)

// entryState represents the state of an entry in the hash map.
type entryState int

const (
	empty entryState = iota
	tombstone
	occupied
)

// entry represents a single entry in the hash map.
type entry struct {
	state entryState
	key   string
	value string
}

// HashMap is a hash map implementation using open addressing with linear probing.
// It provides O(1) average-case complexity for insert, get, and remove operations.
type HashMap struct {
	entries    []entry
	size       int
	tombstones int
}

// New creates a new empty HashMap.
func New() *HashMap {
	return NewWithCapacity(defaultCapacity)
}

// NewWithCapacity creates a new HashMap with the specified capacity.
func NewWithCapacity(capacity int) *HashMap {
	if capacity < defaultCapacity {
		capacity = defaultCapacity
	}
	return &HashMap{
		entries:    make([]entry, capacity),
		size:       0,
		tombstones: 0,
	}
}

// Len returns the number of elements in the map.
func (m *HashMap) Len() int {
	return m.size
}

// IsEmpty returns true if the map contains no elements.
func (m *HashMap) IsEmpty() bool {
	return m.size == 0
}

// Capacity returns the current capacity of the map.
func (m *HashMap) Capacity() int {
	return len(m.entries)
}

func (m *HashMap) hashKey(key string) uint64 {
	return xxhash.Sum64String(key)
}

func (m *HashMap) loadFactor() float64 {
	return float64(m.size+m.tombstones) / float64(len(m.entries))
}

func (m *HashMap) findSlot(key string) (int, bool) {
	hash := m.hashKey(key)
	capacity := len(m.entries)
	index := int(hash % uint64(capacity))
	firstTombstone := -1

	for i := 0; i < capacity; i++ {
		e := &m.entries[index]

		switch e.state {
		case empty:
			if firstTombstone >= 0 {
				return firstTombstone, false
			}
			return index, false

		case tombstone:
			if firstTombstone < 0 {
				firstTombstone = index
			}

		case occupied:
			if e.key == key {
				return index, true
			}
		}

		index = (index + 1) % capacity
	}

	if firstTombstone >= 0 {
		return firstTombstone, false
	}
	return 0, false
}

func (m *HashMap) resize() {
	newCapacity := len(m.entries) * 2
	oldEntries := m.entries

	m.entries = make([]entry, newCapacity)
	m.size = 0
	m.tombstones = 0

	for _, e := range oldEntries {
		if e.state == occupied {
			m.Insert(e.key, e.value)
		}
	}
}

// Insert inserts a key-value pair into the map.
// Returns the previous value and true if the key existed, empty string and false otherwise.
func (m *HashMap) Insert(key, value string) (string, bool) {
	if m.loadFactor() >= maxLoadFactor {
		m.resize()
	}

	index, found := m.findSlot(key)

	if found {
		oldValue := m.entries[index].value
		m.entries[index].value = value
		return oldValue, true
	}

	if m.entries[index].state == tombstone {
		m.tombstones--
	}

	m.entries[index] = entry{
		state: occupied,
		key:   key,
		value: value,
	}
	m.size++
	return "", false
}

// Get retrieves the value associated with the key.
// Returns the value and true if found, empty string and false otherwise.
func (m *HashMap) Get(key string) (string, bool) {
	index, found := m.findSlot(key)
	if found {
		return m.entries[index].value, true
	}
	return "", false
}

// Remove removes a key-value pair from the map.
// Returns the removed value and true if the key existed, empty string and false otherwise.
func (m *HashMap) Remove(key string) (string, bool) {
	index, found := m.findSlot(key)
	if found {
		oldValue := m.entries[index].value
		m.entries[index].state = tombstone
		m.entries[index].key = ""
		m.entries[index].value = ""
		m.size--
		m.tombstones++
		return oldValue, true
	}
	return "", false
}

// Contains checks if the map contains the given key.
func (m *HashMap) Contains(key string) bool {
	_, found := m.findSlot(key)
	return found
}

// Clear removes all entries from the map.
func (m *HashMap) Clear() {
	for i := range m.entries {
		m.entries[i] = entry{}
	}
	m.size = 0
	m.tombstones = 0
}

// Keys returns a slice of all keys in the map.
func (m *HashMap) Keys() []string {
	keys := make([]string, 0, m.size)
	for _, e := range m.entries {
		if e.state == occupied {
			keys = append(keys, e.key)
		}
	}
	return keys
}

// Values returns a slice of all values in the map.
func (m *HashMap) Values() []string {
	values := make([]string, 0, m.size)
	for _, e := range m.entries {
		if e.state == occupied {
			values = append(values, e.value)
		}
	}
	return values
}

// Range iterates over all key-value pairs in the map.
// If f returns false, iteration stops.
func (m *HashMap) Range(f func(key, value string) bool) {
	for _, e := range m.entries {
		if e.state == occupied {
			if !f(e.key, e.value) {
				return
			}
		}
	}
}
