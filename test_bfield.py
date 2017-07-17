"""
Tests for the bfield module.

:author: Zygmunt Krynicki <me@zygoon.pl>
:copyright: Copyright (c) 2017 Zygmunt Krynicki.
:license: MIT
"""

from __future__ import absolute_import

import sys

import doctest
import unittest

try:
    from typing import (cast, Optional, Type, Union)  # noqa: F401
except ImportError:
    pass

import bfield
from bfield import BitField


class BitFieldTests(unittest.TestCase):
    """Unit tests for the BitField type."""

    if sys.version_info[0] == 2:
        assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

    def test_start_equal_to_end(self):
        # type: () -> None
        """Test that empty bit fields raise ValueError."""
        msg = "cannot use start bit equal to end bit"
        with self.assertRaisesRegex(ValueError, msg):
            BitField(0, 0)

    def test_start_greater_than_end(self):
        # type: () -> None
        """Test that "flipped" bit fields raise ValueError."""
        msg = "cannot use start bit greater than end bit"
        with self.assertRaisesRegex(ValueError, msg):
            BitField(1, 0)

    def test_start_bit_negative(self):
        # type: () -> None
        """Test that negative start bit causes ValueError."""
        msg = "cannot use negative start bit"
        with self.assertRaisesRegex(ValueError, msg):
            BitField(-1, 0)

    def test_end_bit_negative(self):
        # type: () -> None
        """Test that negative end bit causes ValueError."""
        msg = "cannot use negative end bit"
        with self.assertRaisesRegex(ValueError, msg):
            BitField(0, -1)

    def test_start_attr(self):
        # type: () -> None
        """Test that the start attribute is valid."""
        self.assertEqual(BitField(5, 7).start, 5)

    def test_end_attr(self):
        # type: () -> None
        """Test that the end attribute is valid."""
        self.assertEqual(BitField(5, 7).end, 7)

    def test_mask_prop(self):
        # type: () -> None
        """Test that the mask property is valid."""
        self.assertEqual(BitField(0, 1).mask, 0b0001)
        self.assertEqual(BitField(0, 2).mask, 0b0011)
        self.assertEqual(BitField(0, 3).mask, 0b0111)
        self.assertEqual(BitField(0, 4).mask, 0b1111)
        self.assertEqual(BitField(1, 2).mask, 0b0010)
        self.assertEqual(BitField(1, 3).mask, 0b0110)
        self.assertEqual(BitField(1, 4).mask, 0b1110)
        self.assertEqual(BitField(2, 3).mask, 0b0100)
        self.assertEqual(BitField(2, 4).mask, 0b1100)
        self.assertEqual(BitField(3, 4).mask, 0b1000)

    def test_getter_class(self):
        # type: () -> None
        """Test that the getter (class) operates as expected."""
        class C(int):
            F = BitField(2, 3)
        F = C.F
        self.assertIsInstance(F, BitField)
        if isinstance(F, BitField):
            self.assertEqual(F.start, 2)
            self.assertEqual(F.end, 3)
            self.assertEqual(F.mask, 0b0100)

    def test_getter_instance(self):
        # type: () -> None
        """Test that the getter (instance) operates as expected."""
        class C(int):
            F = BitField(2, 4)
        value = C(0b1111).F
        self.assertIsInstance(value, int)
        self.assertEqual(value, 0b1100 >> 2)
        self.assertEqual(value, 0b0011 >> 0)
        self.assertEqual(value, 3)

    def test_settr_instance(self):
        # type: () -> None
        """Test that the getter (instance) operates as expected."""
        class C(int):
            F = BitField(2, 4)
        msg = "cannot modify bit-field of immutable int"
        with self.assertRaisesRegex(AttributeError, msg):
            C().F = 0


def load_tests(loader, tests, ignore):
    # type: (unittest.TestLoader, unittest.TestSuite, Optional[str]) -> unittest.TestSuite
    """Add doctests to any loaded unit tests."""
    tests.addTests(doctest.DocTestSuite(bfield))
    return tests


if __name__ == "__main__":
    unittest.main()
