//! Oracle tests comparing our HashMap against std::collections::HashMap

use dsa_lab::HashMap;
use std::collections::HashMap as StdHashMap;

/// Test that our HashMap produces the same results as std HashMap
/// for a sequence of operations.
#[test]
fn test_oracle_insert_get() {
    let mut our_map: HashMap<String, String> = HashMap::new();
    let mut std_map: StdHashMap<String, String> = StdHashMap::new();

    let keys: Vec<String> = (0..1000).map(|i| format!("key_{}", i)).collect();
    let values: Vec<String> = (0..1000).map(|i| format!("value_{}", i)).collect();

    // Insert same data into both maps
    for (key, value) in keys.iter().zip(values.iter()) {
        let our_result = our_map.insert(key.clone(), value.clone());
        let std_result = std_map.insert(key.clone(), value.clone());
        assert_eq!(
            our_result, std_result,
            "Insert results differ for key: {}",
            key
        );
    }

    // Verify same length
    assert_eq!(our_map.len(), std_map.len());

    // Verify same get results
    for key in &keys {
        assert_eq!(
            our_map.get(key),
            std_map.get(key),
            "Get results differ for key: {}",
            key
        );
    }

    // Verify non-existent keys
    assert_eq!(
        our_map.get(&"nonexistent".to_string()),
        std_map.get(&"nonexistent".to_string())
    );
}

#[test]
fn test_oracle_overwrite() {
    let mut our_map: HashMap<String, String> = HashMap::new();
    let mut std_map: StdHashMap<String, String> = StdHashMap::new();

    // Insert initial values
    for i in 0..100 {
        our_map.insert(format!("key_{}", i), format!("value_{}", i));
        std_map.insert(format!("key_{}", i), format!("value_{}", i));
    }

    // Overwrite values
    for i in 0..100 {
        let our_old = our_map.insert(format!("key_{}", i), format!("new_value_{}", i));
        let std_old = std_map.insert(format!("key_{}", i), format!("new_value_{}", i));
        assert_eq!(our_old, std_old);
    }

    // Verify final state
    assert_eq!(our_map.len(), std_map.len());
    for i in 0..100 {
        let key = format!("key_{}", i);
        assert_eq!(our_map.get(&key), std_map.get(&key));
    }
}

#[test]
fn test_oracle_remove() {
    let mut our_map: HashMap<String, String> = HashMap::new();
    let mut std_map: StdHashMap<String, String> = StdHashMap::new();

    // Insert data
    for i in 0..100 {
        our_map.insert(format!("key_{}", i), format!("value_{}", i));
        std_map.insert(format!("key_{}", i), format!("value_{}", i));
    }

    // Remove even keys
    for i in (0..100).step_by(2) {
        let key = format!("key_{}", i);
        let our_removed = our_map.remove(&key);
        let std_removed = std_map.remove(&key);
        assert_eq!(
            our_removed, std_removed,
            "Remove results differ for key: {}",
            key
        );
    }

    // Verify final state
    assert_eq!(our_map.len(), std_map.len());

    for i in 0..100 {
        let key = format!("key_{}", i);
        assert_eq!(
            our_map.get(&key),
            std_map.get(&key),
            "Get after remove differs for key: {}",
            key
        );
        assert_eq!(
            our_map.contains_key(&key),
            std_map.contains_key(&key),
            "Contains_key after remove differs for key: {}",
            key
        );
    }
}

#[test]
fn test_oracle_mixed_operations() {
    use rand::rngs::StdRng;
    use rand::{Rng, SeedableRng};

    let mut rng = StdRng::seed_from_u64(42);
    let mut our_map: HashMap<String, String> = HashMap::new();
    let mut std_map: StdHashMap<String, String> = StdHashMap::new();

    for _ in 0..10000 {
        let op = rng.gen_range(0..3);
        let key = format!("key_{}", rng.gen_range(0..100));
        let value = format!("value_{}", rng.gen_range(0..1000));

        match op {
            0 => {
                // Insert
                let our_result = our_map.insert(key.clone(), value.clone());
                let std_result = std_map.insert(key, value);
                assert_eq!(our_result, std_result);
            }
            1 => {
                // Get
                assert_eq!(our_map.get(&key), std_map.get(&key));
            }
            2 => {
                // Remove
                let our_result = our_map.remove(&key);
                let std_result = std_map.remove(&key);
                assert_eq!(our_result, std_result);
            }
            _ => unreachable!(),
        }
    }

    // Final verification
    assert_eq!(our_map.len(), std_map.len());
}
