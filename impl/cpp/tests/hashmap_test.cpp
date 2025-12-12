#include "hashmap.hpp"
#include <gtest/gtest.h>
#include <string>

using namespace dsa_lab;

class HashMapTest : public ::testing::Test {
protected:
    HashMap<std::string, std::string> map;
};

TEST_F(HashMapTest, NewMapIsEmpty) {
    EXPECT_TRUE(map.empty());
    EXPECT_EQ(map.size(), 0);
}

TEST_F(HashMapTest, InsertAndGet) {
    auto result = map.insert("key1", "value1");
    EXPECT_FALSE(result.has_value());
    EXPECT_EQ(map.get("key1"), "value1");
    EXPECT_EQ(map.size(), 1);
}

TEST_F(HashMapTest, InsertOverwrite) {
    map.insert("key", "value1");
    auto old = map.insert("key", "value2");
    EXPECT_TRUE(old.has_value());
    EXPECT_EQ(old.value(), "value1");
    EXPECT_EQ(map.get("key"), "value2");
    EXPECT_EQ(map.size(), 1);
}

TEST_F(HashMapTest, Remove) {
    map.insert("key", "value");
    auto removed = map.remove("key");
    EXPECT_TRUE(removed.has_value());
    EXPECT_EQ(removed.value(), "value");
    EXPECT_FALSE(map.get("key").has_value());
    EXPECT_TRUE(map.empty());
}

TEST_F(HashMapTest, RemoveNonExistent) {
    auto removed = map.remove("nonexistent");
    EXPECT_FALSE(removed.has_value());
}

TEST_F(HashMapTest, Contains) {
    map.insert("key", "value");
    EXPECT_TRUE(map.contains("key"));
    EXPECT_FALSE(map.contains("other"));
}

TEST_F(HashMapTest, Clear) {
    map.insert("key1", "value1");
    map.insert("key2", "value2");
    map.clear();
    EXPECT_TRUE(map.empty());
    EXPECT_FALSE(map.get("key1").has_value());
}

TEST_F(HashMapTest, Resize) {
    HashMap<std::string, std::string> small_map(4);
    for (int i = 0; i < 100; i++) {
        small_map.insert("key" + std::to_string(i), "value" + std::to_string(i));
    }
    EXPECT_EQ(small_map.size(), 100);
    for (int i = 0; i < 100; i++) {
        EXPECT_EQ(small_map.get("key" + std::to_string(i)), "value" + std::to_string(i));
    }
}

TEST_F(HashMapTest, TombstoneReuse) {
    map.insert("key1", "value1");
    map.insert("key2", "value2");
    map.remove("key1");
    map.insert("key3", "value3");
    EXPECT_EQ(map.size(), 2);
    EXPECT_TRUE(map.contains("key2"));
    EXPECT_TRUE(map.contains("key3"));
    EXPECT_FALSE(map.contains("key1"));
}

TEST_F(HashMapTest, GetPtr) {
    map.insert("key", "value");
    auto* ptr = map.get_ptr("key");
    EXPECT_NE(ptr, nullptr);
    EXPECT_EQ(*ptr, "value");

    *ptr = "modified";
    EXPECT_EQ(map.get("key"), "modified");
}

TEST_F(HashMapTest, GetPtrNonExistent) {
    auto* ptr = map.get_ptr("nonexistent");
    EXPECT_EQ(ptr, nullptr);
}
