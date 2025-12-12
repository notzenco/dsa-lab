#include "hashmap.hpp"
#include <gtest/gtest.h>
#include <random>
#include <string>
#include <unordered_map>

using namespace dsa_lab;

class OracleTest : public ::testing::Test {
protected:
    HashMap<std::string, std::string> our_map;
    std::unordered_map<std::string, std::string> std_map;
};

TEST_F(OracleTest, InsertGet) {
    for (int i = 0; i < 1000; i++) {
        std::string key = "key_" + std::to_string(i);
        std::string value = "value_" + std::to_string(i);

        our_map.insert(key, value);
        std_map[key] = value;
    }

    EXPECT_EQ(our_map.size(), std_map.size());

    for (int i = 0; i < 1000; i++) {
        std::string key = "key_" + std::to_string(i);
        auto our_result = our_map.get(key);
        auto std_it = std_map.find(key);

        ASSERT_TRUE(our_result.has_value());
        ASSERT_NE(std_it, std_map.end());
        EXPECT_EQ(our_result.value(), std_it->second);
    }
}

TEST_F(OracleTest, Overwrite) {
    // Insert initial values
    for (int i = 0; i < 100; i++) {
        std::string key = "key_" + std::to_string(i);
        std::string value = "value_" + std::to_string(i);
        our_map.insert(key, value);
        std_map[key] = value;
    }

    // Overwrite
    for (int i = 0; i < 100; i++) {
        std::string key = "key_" + std::to_string(i);
        std::string new_value = "new_value_" + std::to_string(i);
        our_map.insert(key, new_value);
        std_map[key] = new_value;
    }

    EXPECT_EQ(our_map.size(), std_map.size());

    for (int i = 0; i < 100; i++) {
        std::string key = "key_" + std::to_string(i);
        EXPECT_EQ(our_map.get(key).value(), std_map[key]);
    }
}

TEST_F(OracleTest, Remove) {
    // Insert
    for (int i = 0; i < 100; i++) {
        std::string key = "key_" + std::to_string(i);
        std::string value = "value_" + std::to_string(i);
        our_map.insert(key, value);
        std_map[key] = value;
    }

    // Remove even keys
    for (int i = 0; i < 100; i += 2) {
        std::string key = "key_" + std::to_string(i);
        our_map.remove(key);
        std_map.erase(key);
    }

    EXPECT_EQ(our_map.size(), std_map.size());

    for (int i = 0; i < 100; i++) {
        std::string key = "key_" + std::to_string(i);
        auto our_result = our_map.get(key);
        auto std_it = std_map.find(key);

        if (std_it == std_map.end()) {
            EXPECT_FALSE(our_result.has_value());
        } else {
            ASSERT_TRUE(our_result.has_value());
            EXPECT_EQ(our_result.value(), std_it->second);
        }
    }
}

TEST_F(OracleTest, MixedOperations) {
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> op_dist(0, 2);
    std::uniform_int_distribution<int> key_dist(0, 99);
    std::uniform_int_distribution<int> value_dist(0, 999);

    for (int i = 0; i < 10000; i++) {
        int op = op_dist(rng);
        std::string key = "key_" + std::to_string(key_dist(rng));
        std::string value = "value_" + std::to_string(value_dist(rng));

        switch (op) {
        case 0: // Insert
            our_map.insert(key, value);
            std_map[key] = value;
            break;

        case 1: // Get
            {
                auto our_result = our_map.get(key);
                auto std_it = std_map.find(key);

                if (std_it == std_map.end()) {
                    EXPECT_FALSE(our_result.has_value());
                } else {
                    ASSERT_TRUE(our_result.has_value());
                    EXPECT_EQ(our_result.value(), std_it->second);
                }
            }
            break;

        case 2: // Remove
            our_map.remove(key);
            std_map.erase(key);
            break;
        }
    }

    EXPECT_EQ(our_map.size(), std_map.size());
}
