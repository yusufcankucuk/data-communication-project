
import unittest
import sys
import os
import random
from collections import Counter

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import parity_bit, parity_2d, crc16, hamming_control, internet_checksum
from server import inject_error

class TestUtils(unittest.TestCase):
    def test_parity_bit(self):
        # Even parity
        self.assertEqual(parity_bit("A", "even"), "0") # 'A' is 01000001 (2 ones) -> even -> 0
        self.assertEqual(parity_bit("C", "even"), "1") # 'C' is 01000011 (3 ones) -> even -> 1
        
    def test_parity_2d(self):
        # Basic check to ensure it returns string of correct length
        # 8 rows + 8 cols = 16 bits
        result = parity_2d("12345678")
        self.assertEqual(len(result), 16)
        
    def test_crc16(self):
        # Known CRC16-CCITT (0x1021) values could be checked against online calculators
        # input "123456789" -> 0x29B1 (standard) or similar depending on init value
        # Our implementation uses init 0xFFFF. 
        # Let's just consistency check for now (same input same output)
        res1 = crc16("TEST")
        res2 = crc16("TEST")
        self.assertEqual(res1, res2)
        self.assertNotEqual(crc16("TEST"), crc16("test"))

    def test_hamming(self):
        # Check if it produces 3 bits for every 4 bits of data
        # "A" is 8 bits -> 2 blocks -> 2 * 3 = 6 control bits
        result = hamming_control("A")
        self.assertEqual(len(result), 6)
        
    def test_checksum(self):
        # Consistency check
        self.assertEqual(internet_checksum("TEST"), internet_checksum("TEST"))

class TestServerLogic(unittest.TestCase):
    def test_error_injection_types(self):
        data = "HELLO_WORLD_TEST_STRING"
        
        # Test each specific error type
        # We need to access the internal functions of server.py or use inject_error ensuring specific type
        
        # 1. Bit Flip
        corrupted, name = inject_error(data, 1)
        self.assertEqual(name, "Bit Flip")
        self.assertNotEqual(data, corrupted)
        
        # 2. Substitution
        corrupted, name = inject_error(data, 2)
        self.assertEqual(name, "Character Substitution")
        self.assertEqual(len(data), len(corrupted))
        self.assertNotEqual(data, corrupted)
        
        # 3. Deletion
        corrupted, name = inject_error(data, 3)
        self.assertEqual(name, "Character Deletion")
        self.assertEqual(len(data) - 1, len(corrupted))
        
        # 4. Insertion
        corrupted, name = inject_error(data, 4)
        self.assertEqual(name, "Character Insertion")
        self.assertEqual(len(data) + 1, len(corrupted))
        
        # 5. Swapping
        corrupted, name = inject_error(data, 5)
        self.assertEqual(name, "Character Swapping")
        self.assertEqual(len(data), len(corrupted))
        self.assertNotEqual(data, corrupted)
        
        # 6. Multi Bit Flip
        corrupted, name = inject_error(data, 6)
        self.assertEqual(name, "Multiple Bit Flips")
        self.assertNotEqual(data, corrupted)
        
        # 7. Burst
        corrupted, name = inject_error(data, 7)
        self.assertEqual(name, "Burst Error")
        self.assertEqual(len(data), len(corrupted))
        self.assertNotEqual(data, corrupted)

if __name__ == '__main__':
    unittest.main()
