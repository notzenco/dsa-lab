package bench

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"testing"

	"github.com/dsa-lab/go/internal/hashmap"
)

type Operation struct {
	Op    string `json:"op"`
	Key   string `json:"key"`
	Value string `json:"value,omitempty"`
}

type Workload struct {
	Name       string      `json:"name"`
	Size       int         `json:"size"`
	Operations []Operation `json:"operations"`
}

func loadWorkload(name string) (*Workload, error) {
	// Try multiple paths
	paths := []string{
		filepath.Join("..", "..", "workloads", "map", name+".json"),
		filepath.Join("..", "..", "..", "workloads", "map", name+".json"),
	}

	var data []byte
	var err error
	for _, path := range paths {
		data, err = os.ReadFile(path)
		if err == nil {
			break
		}
	}
	if err != nil {
		return nil, err
	}

	var workload Workload
	if err := json.Unmarshal(data, &workload); err != nil {
		return nil, err
	}
	return &workload, nil
}

func BenchmarkInsert(b *testing.B) {
	sizes := []int{100, 1000, 10000}

	for _, size := range sizes {
		keys := make([]string, size)
		values := make([]string, size)
		for i := 0; i < size; i++ {
			keys[i] = fmt.Sprintf("key_%d", i)
			values[i] = fmt.Sprintf("value_%d", i)
		}

		b.Run(fmt.Sprintf("size=%d", size), func(b *testing.B) {
			b.ResetTimer()
			for i := 0; i < b.N; i++ {
				m := hashmap.New()
				for j := 0; j < size; j++ {
					m.Insert(keys[j], values[j])
				}
			}
		})
	}
}

func BenchmarkGet(b *testing.B) {
	sizes := []int{100, 1000, 10000}

	for _, size := range sizes {
		keys := make([]string, size)
		m := hashmap.New()
		for i := 0; i < size; i++ {
			keys[i] = fmt.Sprintf("key_%d", i)
			m.Insert(keys[i], fmt.Sprintf("value_%d", i))
		}

		b.Run(fmt.Sprintf("size=%d", size), func(b *testing.B) {
			b.ResetTimer()
			for i := 0; i < b.N; i++ {
				for _, key := range keys {
					m.Get(key)
				}
			}
		})
	}
}

func BenchmarkMixedUniformMedium(b *testing.B) {
	workload, err := loadWorkload("mixed_uniform_medium")
	if err != nil {
		b.Skip("workload not found:", err)
		return
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		m := hashmap.New()
		for _, op := range workload.Operations {
			switch op.Op {
			case "insert":
				m.Insert(op.Key, op.Value)
			case "get":
				m.Get(op.Key)
			case "delete":
				m.Remove(op.Key)
			}
		}
	}
}

func BenchmarkInsertHeavyUniformMedium(b *testing.B) {
	workload, err := loadWorkload("insert_heavy_uniform_medium")
	if err != nil {
		b.Skip("workload not found:", err)
		return
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		m := hashmap.New()
		for _, op := range workload.Operations {
			if op.Op == "insert" {
				m.Insert(op.Key, op.Value)
			}
		}
	}
}

func BenchmarkReadHeavyUniformMedium(b *testing.B) {
	workload, err := loadWorkload("read_heavy_uniform_medium")
	if err != nil {
		b.Skip("workload not found:", err)
		return
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		m := hashmap.New()
		for _, op := range workload.Operations {
			switch op.Op {
			case "insert":
				m.Insert(op.Key, op.Value)
			case "get":
				m.Get(op.Key)
			}
		}
	}
}
