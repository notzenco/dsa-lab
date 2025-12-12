#pragma once

#include <cstddef>
#include <functional>
#include <optional>
#include <string>
#include <vector>

namespace dsa_lab {

constexpr size_t kDefaultCapacity = 16;
constexpr double kMaxLoadFactor = 0.75;

/// Entry state in the hash map
enum class EntryState { Empty, Tombstone, Occupied };

/// A single entry in the hash map
template <typename K, typename V>
struct Entry {
    EntryState state = EntryState::Empty;
    K key;
    V value;
};

/// Hash map implementation using open addressing with linear probing.
///
/// Provides O(1) average-case complexity for insert, get, and remove operations.
template <typename K, typename V, typename Hash = std::hash<K>>
class HashMap {
public:
    /// Create a new empty HashMap.
    HashMap() : HashMap(kDefaultCapacity) {}

    /// Create a new HashMap with the specified capacity.
    explicit HashMap(size_t capacity)
        : entries_(std::max(capacity, kDefaultCapacity)),
          size_(0),
          tombstones_(0) {}

    /// Returns the number of elements in the map.
    [[nodiscard]] size_t size() const { return size_; }

    /// Returns true if the map contains no elements.
    [[nodiscard]] bool empty() const { return size_ == 0; }

    /// Returns the current capacity of the map.
    [[nodiscard]] size_t capacity() const { return entries_.size(); }

    /// Insert a key-value pair into the map.
    /// Returns the previous value if the key existed.
    std::optional<V> insert(const K& key, const V& value) {
        if (load_factor() >= kMaxLoadFactor) {
            resize();
        }

        auto [index, found] = find_slot(key);

        if (found) {
            V old_value = entries_[index].value;
            entries_[index].value = value;
            return old_value;
        }

        if (entries_[index].state == EntryState::Tombstone) {
            tombstones_--;
        }

        entries_[index].state = EntryState::Occupied;
        entries_[index].key = key;
        entries_[index].value = value;
        size_++;
        return std::nullopt;
    }

    /// Get the value associated with the key.
    [[nodiscard]] std::optional<V> get(const K& key) const {
        auto [index, found] = find_slot(key);
        if (found) {
            return entries_[index].value;
        }
        return std::nullopt;
    }

    /// Get a pointer to the value associated with the key.
    [[nodiscard]] V* get_ptr(const K& key) {
        auto [index, found] = find_slot(key);
        if (found) {
            return &entries_[index].value;
        }
        return nullptr;
    }

    /// Remove a key-value pair from the map.
    /// Returns the removed value if the key existed.
    std::optional<V> remove(const K& key) {
        auto [index, found] = find_slot(key);
        if (found) {
            V old_value = entries_[index].value;
            entries_[index].state = EntryState::Tombstone;
            size_--;
            tombstones_++;
            return old_value;
        }
        return std::nullopt;
    }

    /// Check if the map contains the given key.
    [[nodiscard]] bool contains(const K& key) const {
        auto [_, found] = find_slot(key);
        return found;
    }

    /// Clear all entries from the map.
    void clear() {
        for (auto& entry : entries_) {
            entry.state = EntryState::Empty;
        }
        size_ = 0;
        tombstones_ = 0;
    }

private:
    std::vector<Entry<K, V>> entries_;
    size_t size_;
    size_t tombstones_;
    Hash hasher_;

    [[nodiscard]] double load_factor() const {
        return static_cast<double>(size_ + tombstones_) /
               static_cast<double>(entries_.size());
    }

    [[nodiscard]] size_t hash_key(const K& key) const {
        return hasher_(key);
    }

    [[nodiscard]] std::pair<size_t, bool> find_slot(const K& key) const {
        size_t hash = hash_key(key);
        size_t cap = entries_.size();
        size_t index = hash % cap;
        std::optional<size_t> first_tombstone;

        for (size_t i = 0; i < cap; i++) {
            const auto& entry = entries_[index];

            switch (entry.state) {
            case EntryState::Empty:
                return {first_tombstone.value_or(index), false};

            case EntryState::Tombstone:
                if (!first_tombstone) {
                    first_tombstone = index;
                }
                break;

            case EntryState::Occupied:
                if (entry.key == key) {
                    return {index, true};
                }
                break;
            }

            index = (index + 1) % cap;
        }

        return {first_tombstone.value_or(0), false};
    }

    void resize() {
        size_t new_capacity = entries_.size() * 2;
        std::vector<Entry<K, V>> old_entries = std::move(entries_);

        entries_ = std::vector<Entry<K, V>>(new_capacity);
        size_ = 0;
        tombstones_ = 0;

        for (auto& entry : old_entries) {
            if (entry.state == EntryState::Occupied) {
                insert(entry.key, entry.value);
            }
        }
    }
};

} // namespace dsa_lab
