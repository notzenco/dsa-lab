//! Hash Map implementation using open addressing with linear probing.

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

const DEFAULT_CAPACITY: usize = 16;
const MAX_LOAD_FACTOR: f64 = 0.75;

#[derive(Debug, Clone)]
enum Entry<K, V> {
    Empty,
    Tombstone,
    Occupied { key: K, value: V },
}

impl<K, V> Entry<K, V> {
    fn is_tombstone(&self) -> bool {
        matches!(self, Entry::Tombstone)
    }
}

/// A hash map implementation using open addressing with linear probing.
///
/// This implementation provides O(1) average-case complexity for insert, get,
/// and remove operations.
#[derive(Debug, Clone)]
pub struct HashMap<K, V> {
    entries: Vec<Entry<K, V>>,
    size: usize,
    tombstones: usize,
}

impl<K, V> Default for HashMap<K, V>
where
    K: Hash + Eq + Clone,
    V: Clone,
{
    fn default() -> Self {
        Self::new()
    }
}

impl<K, V> HashMap<K, V>
where
    K: Hash + Eq + Clone,
    V: Clone,
{
    /// Create a new empty HashMap.
    pub fn new() -> Self {
        Self::with_capacity(DEFAULT_CAPACITY)
    }

    /// Create a new HashMap with the specified capacity.
    pub fn with_capacity(capacity: usize) -> Self {
        let capacity = capacity.max(DEFAULT_CAPACITY);
        let mut entries = Vec::with_capacity(capacity);
        entries.resize_with(capacity, || Entry::Empty);
        Self {
            entries,
            size: 0,
            tombstones: 0,
        }
    }

    /// Returns the number of elements in the map.
    pub fn len(&self) -> usize {
        self.size
    }

    /// Returns true if the map contains no elements.
    pub fn is_empty(&self) -> bool {
        self.size == 0
    }

    /// Returns the current capacity of the map.
    pub fn capacity(&self) -> usize {
        self.entries.len()
    }

    fn hash_key(&self, key: &K) -> usize {
        let mut hasher = DefaultHasher::new();
        key.hash(&mut hasher);
        hasher.finish() as usize
    }

    fn load_factor(&self) -> f64 {
        (self.size + self.tombstones) as f64 / self.entries.len() as f64
    }

    fn find_slot(&self, key: &K) -> (usize, bool) {
        let hash = self.hash_key(key);
        let capacity = self.entries.len();
        let mut index = hash % capacity;
        let mut first_tombstone: Option<usize> = None;

        for _ in 0..capacity {
            match &self.entries[index] {
                Entry::Empty => {
                    return (first_tombstone.unwrap_or(index), false);
                }
                Entry::Tombstone => {
                    if first_tombstone.is_none() {
                        first_tombstone = Some(index);
                    }
                }
                Entry::Occupied { key: k, .. } if k == key => {
                    return (index, true);
                }
                Entry::Occupied { .. } => {}
            }
            index = (index + 1) % capacity;
        }

        (first_tombstone.unwrap_or(0), false)
    }

    fn resize(&mut self) {
        let new_capacity = self.entries.len() * 2;
        let old_entries = std::mem::replace(&mut self.entries, {
            let mut v = Vec::with_capacity(new_capacity);
            v.resize_with(new_capacity, || Entry::Empty);
            v
        });

        self.size = 0;
        self.tombstones = 0;

        for entry in old_entries {
            if let Entry::Occupied { key, value } = entry {
                self.insert(key, value);
            }
        }
    }

    /// Insert a key-value pair into the map.
    ///
    /// Returns the previous value if the key existed.
    pub fn insert(&mut self, key: K, value: V) -> Option<V> {
        if self.load_factor() >= MAX_LOAD_FACTOR {
            self.resize();
        }

        let (index, found) = self.find_slot(&key);

        if found {
            if let Entry::Occupied {
                value: old_value, ..
            } = &mut self.entries[index]
            {
                let prev = old_value.clone();
                *old_value = value;
                return Some(prev);
            }
        }

        if self.entries[index].is_tombstone() {
            self.tombstones -= 1;
        }

        self.entries[index] = Entry::Occupied { key, value };
        self.size += 1;
        None
    }

    /// Get a reference to the value associated with the key.
    pub fn get(&self, key: &K) -> Option<&V> {
        let (index, found) = self.find_slot(key);
        if found {
            if let Entry::Occupied { value, .. } = &self.entries[index] {
                return Some(value);
            }
        }
        None
    }

    /// Get a mutable reference to the value associated with the key.
    pub fn get_mut(&mut self, key: &K) -> Option<&mut V> {
        let (index, found) = self.find_slot(key);
        if found {
            if let Entry::Occupied { value, .. } = &mut self.entries[index] {
                return Some(value);
            }
        }
        None
    }

    /// Remove a key-value pair from the map.
    ///
    /// Returns the removed value if the key existed.
    pub fn remove(&mut self, key: &K) -> Option<V> {
        let (index, found) = self.find_slot(key);
        if found {
            let entry = std::mem::replace(&mut self.entries[index], Entry::Tombstone);
            if let Entry::Occupied { value, .. } = entry {
                self.size -= 1;
                self.tombstones += 1;
                return Some(value);
            }
        }
        None
    }

    /// Check if the map contains the given key.
    pub fn contains_key(&self, key: &K) -> bool {
        let (_, found) = self.find_slot(key);
        found
    }

    /// Clear all entries from the map.
    pub fn clear(&mut self) {
        for entry in &mut self.entries {
            *entry = Entry::Empty;
        }
        self.size = 0;
        self.tombstones = 0;
    }

    /// Iterate over all key-value pairs.
    pub fn iter(&self) -> impl Iterator<Item = (&K, &V)> {
        self.entries.iter().filter_map(|entry| {
            if let Entry::Occupied { key, value } = entry {
                Some((key, value))
            } else {
                None
            }
        })
    }

    /// Iterate over all keys.
    pub fn keys(&self) -> impl Iterator<Item = &K> {
        self.iter().map(|(k, _)| k)
    }

    /// Iterate over all values.
    pub fn values(&self) -> impl Iterator<Item = &V> {
        self.iter().map(|(_, v)| v)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new() {
        let map: HashMap<String, String> = HashMap::new();
        assert!(map.is_empty());
        assert_eq!(map.len(), 0);
    }

    #[test]
    fn test_insert_and_get() {
        let mut map = HashMap::new();
        assert!(map
            .insert("key1".to_string(), "value1".to_string())
            .is_none());
        assert_eq!(map.get(&"key1".to_string()), Some(&"value1".to_string()));
        assert_eq!(map.len(), 1);
    }

    #[test]
    fn test_insert_overwrite() {
        let mut map = HashMap::new();
        map.insert("key".to_string(), "value1".to_string());
        let old = map.insert("key".to_string(), "value2".to_string());
        assert_eq!(old, Some("value1".to_string()));
        assert_eq!(map.get(&"key".to_string()), Some(&"value2".to_string()));
        assert_eq!(map.len(), 1);
    }

    #[test]
    fn test_remove() {
        let mut map = HashMap::new();
        map.insert("key".to_string(), "value".to_string());
        let removed = map.remove(&"key".to_string());
        assert_eq!(removed, Some("value".to_string()));
        assert!(map.get(&"key".to_string()).is_none());
        assert!(map.is_empty());
    }

    #[test]
    fn test_contains_key() {
        let mut map = HashMap::new();
        map.insert("key".to_string(), "value".to_string());
        assert!(map.contains_key(&"key".to_string()));
        assert!(!map.contains_key(&"other".to_string()));
    }

    #[test]
    fn test_clear() {
        let mut map = HashMap::new();
        map.insert("key1".to_string(), "value1".to_string());
        map.insert("key2".to_string(), "value2".to_string());
        map.clear();
        assert!(map.is_empty());
        assert!(map.get(&"key1".to_string()).is_none());
    }

    #[test]
    fn test_resize() {
        let mut map = HashMap::with_capacity(4);
        for i in 0..100 {
            map.insert(format!("key{}", i), format!("value{}", i));
        }
        assert_eq!(map.len(), 100);
        for i in 0..100 {
            assert_eq!(map.get(&format!("key{}", i)), Some(&format!("value{}", i)));
        }
    }

    #[test]
    fn test_tombstone_reuse() {
        let mut map = HashMap::new();
        map.insert("key1".to_string(), "value1".to_string());
        map.insert("key2".to_string(), "value2".to_string());
        map.remove(&"key1".to_string());
        map.insert("key3".to_string(), "value3".to_string());
        assert_eq!(map.len(), 2);
        assert!(map.contains_key(&"key2".to_string()));
        assert!(map.contains_key(&"key3".to_string()));
    }
}
