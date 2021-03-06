import unittest

from bxcommon.utils.crypto import SHA256_HASH_LEN
from bxcommon.utils.object_hash import Sha256Hash


class ObjectHashTests(unittest.TestCase):
    to_31 = bytearray([i for i in range(SHA256_HASH_LEN)])

    def setUp(self):
        self.int_hash_31a = Sha256Hash(self.to_31)
        self.int_hash_31b = Sha256Hash(memoryview(self.to_31))
        self.int_hash_32 = Sha256Hash(bytearray([i for i in range(1, SHA256_HASH_LEN + 1)]))
        self.int_hash_all_0 = Sha256Hash(bytearray([0] * SHA256_HASH_LEN))

    def test_init(self):
        with self.assertRaises(ValueError):
            Sha256Hash(bytearray([i for i in range(SHA256_HASH_LEN - 1)]))
        with self.assertRaises(ValueError):
            Sha256Hash(bytearray())

        expected = self.int_hash_31a.binary
        actual = self.to_31
        self.assertEqual(expected, actual)
        actual = Sha256Hash(memoryview(actual))
        self.assertEqual(expected, actual.binary)
        self.assertIsNotNone(hash(self.int_hash_all_0))

    def test_hash(self):
        self.assertEqual(hash(self.int_hash_31a), hash(self.int_hash_31b))
        self.assertNotEqual(hash(self.int_hash_31a), hash(self.int_hash_32))
        # checking that hash does not change when byte array is mutated
        to_31 = bytearray([i for i in range(SHA256_HASH_LEN)])
        mutable_to_31 = Sha256Hash(to_31)
        initial_hash = hash(mutable_to_31)
        to_31[6] = 12
        mutated_hash = hash(mutable_to_31)
        self.assertEqual(initial_hash, mutated_hash)

    def test_cmp(self):
        self.assertEqual(self.int_hash_31a, self.int_hash_31b)
        self.assertGreater(self.int_hash_32, self.int_hash_31a)
        self.assertLess(self.int_hash_all_0, self.int_hash_31b)

    def test_get_item(self):
        int_list = [0] * SHA256_HASH_LEN
        expected_1 = 3
        expected_index_1 = 1
        expected_2 = 9
        expected_index_2 = 8
        int_list[expected_index_1] = expected_1
        int_list[expected_index_2] = expected_2
        int_hash = Sha256Hash(bytearray(int_list))
        self.assertEqual(expected_1, int_hash[expected_index_1])
        self.assertEqual(expected_2, int_hash[expected_index_2])

    def test_repr(self):
        self.assertEqual(repr(self.int_hash_31a), repr(self.int_hash_31b))
        self.assertNotEqual(repr(self.int_hash_31a), repr(self.int_hash_32))
        self.assertNotEqual(repr(self.int_hash_31b), repr(self.int_hash_all_0))
