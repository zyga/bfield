
===============
bfield.BitField
===============

The missing bitfield type for Python 2 and 3.

Example
=======

The following example illustrates possible use of bfield::

  from bfield import BitField

  class AX(int):
      AL = BitField(0, 8, "The lower octet")
      AH = BitField(8, 16, "The higher octet")


  assert AX(0x1234).AH == 0x12
  assert AX(0x1234).AL == 0x34

Caveat
======

Note that due to specifics of immutable ints, read-only is the best thing
available. This is sufficient for decoding binary protocols and file formats.
