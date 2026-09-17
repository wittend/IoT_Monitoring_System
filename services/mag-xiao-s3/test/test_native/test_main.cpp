/*
 * test_main.cpp — Host-native unit tests for mag-xiao-s3
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Copyright (C) 2020-2025 David Witten
 */
#include <unity.h>

void setUp(void) {}
void tearDown(void) {}

static void test_addition(void) {
    TEST_ASSERT_EQUAL_INT(4, 2 + 2);
}

int main(int argc, char **argv) {
    UNITY_BEGIN();
    RUN_TEST(test_addition);
    return UNITY_END();
}
