"""
The bfield module provides definition of the BitField type.

The BitField type assists in extracting bit ranges from integers. A class
inheriting from the int type may declare any number of named BitField
attributes and use them to access designated bits or bit ranges.

:author: Zygmunt Krynicki <me@zygoon.pl>
:copyright: Copyright (c) 2017 Zygmunt Krynicki.
:license: MIT
"""

try:
    from typing import (cast, Optional, Type, Union)  # noqa: F401
except ImportError:
    pass


__all__ = ('BitField', )


class BitField(object):
    """
    Bit field within an integer.

    Bit fields are common in many binary protocols and data formats. This class
    aids in declaring and extracting bit fields.

    Using a subclass of int define any number of BitField objects with desired
    bit spans and then access them through the instance of the class.

    >>> class AX(int):
    ...     '''The x86 AX register.'''
    ...
    ...     AH = BitField(8, 16, "The higher octet")
    ...     AL = BitField(0, 8, "The lower octet")

    Individual values can now be extracted by referring to their field names.

    >>> hex(AX(0x1234).AH)
    '0x12'
    >>> hex(AX(0x1234).AL)
    '0x34'

    Each bit field comes with a handy mask accessible from the class.

    >>> hex(AX.AH.mask)
    '0xff00'

    You can also access the low and high bit numbers.

    >>> AX.AH.start, AX.AH.end
    (8, 16)
    """

    def __init__(self, start, end, doc=None):
        # type: (int, int, Optional[str]) -> None
        """
        Initialize the bit field.

        :arg start:
            Number of the starting bit (inclusive).
        :arg end:
            Number of the ending bit (exclusive).
        :arg doc:
            Optional documentation string.
        :raises ValueError:
            When start and end are incorrectly specified.

        Start and end denote the start (inclusive) and end bits (exclusive).
        Neither number may be negative and they must describe non-empty range
        of bits.
        """
        if start < 0:
            raise ValueError("cannot use negative start bit")
        if end < 0:
            raise ValueError("cannot use negative end bit")
        if start > end:
            raise ValueError("cannot use start bit greater than end bit")
        if start == end:
            raise ValueError("cannot use start bit equal to end bit")
        self.start = start  # type: int
        self.end = end  # type: int
        self.mask = (1 << end) - (1 << start)  # type: int
        if doc is not None:
            self.__doc__ = doc

    def __set__(self, instance, value):
        # type: (object, int) -> None
        """
        Set bit field to specified value (dummy).

        Bit fields are defined on subclasses of int, which is read-only and
        cannot be changed. As such, bit-fields provide a set method to
        explain this fact to the developer.

        As a separate reason, pydoc shows documentation strings only if both
        __get__ and __set__ exist.
        """
        raise AttributeError("cannot modify bit-field of immutable int")

    def __get__(self, instance, owner):
        # type: (Optional[object], Type) -> Union[BitField, int]
        """
        Extract bit-field value (instance) or return BitField object (class).

        :returns:
            BitField object or the extracted value.
        :raises TypeError:
            When accessed through a class not derived from int.

        The returned value is either the BitField instance, when accessed
        through class, or masked and right-shifted value of the bit field, when
        accessed through instance.
        """
        if instance is None:
            return self
        if not isinstance(instance, int):
            raise TypeError("cannot get value from non-int instance object"
                            " {}".format(type(instance)))
        return (instance & self.mask) >> self.start
