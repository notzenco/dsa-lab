package hashmap

import (
	"fmt"
	"testing"
)

func TestNew(t *testing.T) {
	m := New()
	if !m.IsEmpty() {
		t.Error("new map should be empty")
	}
	if m.Len() != 0 {
		t.Errorf("new map should have length 0, got %d", m.Len())
	}
}

func TestInsertAndGet(t *testing.T) {
	m := New()
	old, existed := m.Insert("key1", "value1")
	if existed {
		t.Error("insert to new map should not return existing value")
	}
	if old != "" {
		t.Errorf("old value should be empty, got %s", old)
	}

	value, found := m.Get("key1")
	if !found {
		t.Error("get should find inserted key")
	}
	if value != "value1" {
		t.Errorf("expected value1, got %s", value)
	}
	if m.Len() != 1 {
		t.Errorf("expected length 1, got %d", m.Len())
	}
}

func TestInsertOverwrite(t *testing.T) {
	m := New()
	m.Insert("key", "value1")
	old, existed := m.Insert("key", "value2")

	if !existed {
		t.Error("overwrite should return existed=true")
	}
	if old != "value1" {
		t.Errorf("expected old value 'value1', got '%s'", old)
	}

	value, _ := m.Get("key")
	if value != "value2" {
		t.Errorf("expected value2, got %s", value)
	}
	if m.Len() != 1 {
		t.Errorf("expected length 1, got %d", m.Len())
	}
}

func TestRemove(t *testing.T) {
	m := New()
	m.Insert("key", "value")
	removed, existed := m.Remove("key")

	if !existed {
		t.Error("remove should return existed=true for existing key")
	}
	if removed != "value" {
		t.Errorf("expected removed value 'value', got '%s'", removed)
	}

	_, found := m.Get("key")
	if found {
		t.Error("get should not find removed key")
	}
	if !m.IsEmpty() {
		t.Error("map should be empty after removing only element")
	}
}

func TestRemoveNonExistent(t *testing.T) {
	m := New()
	_, existed := m.Remove("nonexistent")
	if existed {
		t.Error("remove should return existed=false for non-existent key")
	}
}

func TestContains(t *testing.T) {
	m := New()
	m.Insert("key", "value")

	if !m.Contains("key") {
		t.Error("contains should return true for existing key")
	}
	if m.Contains("other") {
		t.Error("contains should return false for non-existent key")
	}
}

func TestClear(t *testing.T) {
	m := New()
	m.Insert("key1", "value1")
	m.Insert("key2", "value2")
	m.Clear()

	if !m.IsEmpty() {
		t.Error("map should be empty after clear")
	}
	if _, found := m.Get("key1"); found {
		t.Error("cleared map should not contain keys")
	}
}

func TestResize(t *testing.T) {
	m := NewWithCapacity(4)
	for i := 0; i < 100; i++ {
		m.Insert(fmt.Sprintf("key%d", i), fmt.Sprintf("value%d", i))
	}

	if m.Len() != 100 {
		t.Errorf("expected length 100, got %d", m.Len())
	}

	for i := 0; i < 100; i++ {
		key := fmt.Sprintf("key%d", i)
		expected := fmt.Sprintf("value%d", i)
		value, found := m.Get(key)
		if !found {
			t.Errorf("key %s not found after resize", key)
		}
		if value != expected {
			t.Errorf("expected %s, got %s", expected, value)
		}
	}
}

func TestTombstoneReuse(t *testing.T) {
	m := New()
	m.Insert("key1", "value1")
	m.Insert("key2", "value2")
	m.Remove("key1")
	m.Insert("key3", "value3")

	if m.Len() != 2 {
		t.Errorf("expected length 2, got %d", m.Len())
	}
	if !m.Contains("key2") {
		t.Error("key2 should exist")
	}
	if !m.Contains("key3") {
		t.Error("key3 should exist")
	}
	if m.Contains("key1") {
		t.Error("key1 should not exist")
	}
}

func TestKeysAndValues(t *testing.T) {
	m := New()
	m.Insert("a", "1")
	m.Insert("b", "2")
	m.Insert("c", "3")

	keys := m.Keys()
	if len(keys) != 3 {
		t.Errorf("expected 3 keys, got %d", len(keys))
	}

	values := m.Values()
	if len(values) != 3 {
		t.Errorf("expected 3 values, got %d", len(values))
	}
}

func TestRange(t *testing.T) {
	m := New()
	m.Insert("a", "1")
	m.Insert("b", "2")
	m.Insert("c", "3")

	count := 0
	m.Range(func(key, value string) bool {
		count++
		return true
	})

	if count != 3 {
		t.Errorf("range should iterate 3 times, got %d", count)
	}

	// Test early exit
	count = 0
	m.Range(func(key, value string) bool {
		count++
		return count < 2
	})

	if count != 2 {
		t.Errorf("range should stop after 2 iterations, got %d", count)
	}
}
