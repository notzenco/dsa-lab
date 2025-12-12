package tests

import (
	"fmt"
	"math/rand"
	"testing"

	"github.com/dsa-lab/go/internal/hashmap"
)

func TestOracleInsertGet(t *testing.T) {
	ourMap := hashmap.New()
	stdMap := make(map[string]string)

	for i := 0; i < 1000; i++ {
		key := fmt.Sprintf("key_%d", i)
		value := fmt.Sprintf("value_%d", i)

		ourMap.Insert(key, value)
		stdMap[key] = value
	}

	if ourMap.Len() != len(stdMap) {
		t.Errorf("length mismatch: our=%d, std=%d", ourMap.Len(), len(stdMap))
	}

	for i := 0; i < 1000; i++ {
		key := fmt.Sprintf("key_%d", i)
		ourValue, ourFound := ourMap.Get(key)
		stdValue, stdFound := stdMap[key]

		if ourFound != stdFound {
			t.Errorf("found mismatch for key %s: our=%v, std=%v", key, ourFound, stdFound)
		}
		if ourValue != stdValue {
			t.Errorf("value mismatch for key %s: our=%s, std=%s", key, ourValue, stdValue)
		}
	}

	// Test non-existent key
	_, ourFound := ourMap.Get("nonexistent")
	_, stdFound := stdMap["nonexistent"]
	if ourFound != stdFound {
		t.Error("non-existent key should return same result")
	}
}

func TestOracleOverwrite(t *testing.T) {
	ourMap := hashmap.New()
	stdMap := make(map[string]string)

	// Insert initial values
	for i := 0; i < 100; i++ {
		key := fmt.Sprintf("key_%d", i)
		value := fmt.Sprintf("value_%d", i)
		ourMap.Insert(key, value)
		stdMap[key] = value
	}

	// Overwrite
	for i := 0; i < 100; i++ {
		key := fmt.Sprintf("key_%d", i)
		newValue := fmt.Sprintf("new_value_%d", i)
		ourMap.Insert(key, newValue)
		stdMap[key] = newValue
	}

	if ourMap.Len() != len(stdMap) {
		t.Errorf("length mismatch: our=%d, std=%d", ourMap.Len(), len(stdMap))
	}

	for i := 0; i < 100; i++ {
		key := fmt.Sprintf("key_%d", i)
		ourValue, _ := ourMap.Get(key)
		if ourValue != stdMap[key] {
			t.Errorf("value mismatch for key %s", key)
		}
	}
}

func TestOracleRemove(t *testing.T) {
	ourMap := hashmap.New()
	stdMap := make(map[string]string)

	// Insert
	for i := 0; i < 100; i++ {
		key := fmt.Sprintf("key_%d", i)
		value := fmt.Sprintf("value_%d", i)
		ourMap.Insert(key, value)
		stdMap[key] = value
	}

	// Remove even keys
	for i := 0; i < 100; i += 2 {
		key := fmt.Sprintf("key_%d", i)
		ourMap.Remove(key)
		delete(stdMap, key)
	}

	if ourMap.Len() != len(stdMap) {
		t.Errorf("length mismatch: our=%d, std=%d", ourMap.Len(), len(stdMap))
	}

	for i := 0; i < 100; i++ {
		key := fmt.Sprintf("key_%d", i)
		ourValue, ourFound := ourMap.Get(key)
		stdValue, stdFound := stdMap[key]

		if ourFound != stdFound {
			t.Errorf("found mismatch for key %s: our=%v, std=%v", key, ourFound, stdFound)
		}
		if ourFound && ourValue != stdValue {
			t.Errorf("value mismatch for key %s: our=%s, std=%s", key, ourValue, stdValue)
		}
	}
}

func TestOracleMixedOperations(t *testing.T) {
	rng := rand.New(rand.NewSource(42))
	ourMap := hashmap.New()
	stdMap := make(map[string]string)

	for i := 0; i < 10000; i++ {
		op := rng.Intn(3)
		key := fmt.Sprintf("key_%d", rng.Intn(100))
		value := fmt.Sprintf("value_%d", rng.Intn(1000))

		switch op {
		case 0: // Insert
			ourMap.Insert(key, value)
			stdMap[key] = value

		case 1: // Get
			ourValue, ourFound := ourMap.Get(key)
			stdValue, stdFound := stdMap[key]
			if ourFound != stdFound {
				t.Errorf("found mismatch for key %s at iteration %d", key, i)
			}
			if ourFound && ourValue != stdValue {
				t.Errorf("value mismatch for key %s at iteration %d", key, i)
			}

		case 2: // Remove
			ourMap.Remove(key)
			delete(stdMap, key)
		}
	}

	if ourMap.Len() != len(stdMap) {
		t.Errorf("final length mismatch: our=%d, std=%d", ourMap.Len(), len(stdMap))
	}
}
