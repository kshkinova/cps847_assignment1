import unittest

import sample

class TestMethods(unittest.TestCase):
    def test_add(self):
        self.assertEqual(sample.add(), 8);

    def test_subtract(self):
        self.assertEqual(sample.subtract(), 4);

    def test_multiply(self):
        self.assertEqual(sample.multiply(), 25);




if __name__ == '__main__':
    unittest.main()
