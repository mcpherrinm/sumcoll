#!/usr/bin/env python3

### Sum.py
### An implementation of the BSD `sum` checksum in python.

import math, sys
from typing import Iterable, Tuple

def rotate_right_16bit(data: int) -> int:
  """rotate a 16-bit value to the right"""
  return (data >> 1) | ((data & 1) << 15)

def add(sum: int, byte: int) -> int:
  sum = rotate_right_16bit(sum) + byte
  return sum & 0xffff # clamp to 16 bits

def compute_sum(data: bytes) -> Tuple[int, int]:
  """
  Compute the BSD sum checksum over data

  Returns the checksum and number of 1024 byte blocks
  """
  sum = 0
  for byte in data:
    sum = add(sum, byte)
  return sum, math.ceil(len(data) / 1024)

def format_sum(sum: int, blocks: int):
  """Format checksum and block count like sum does"""
  return "{:05} {:5}".format(sum, blocks)

if __name__ == "__main__":
  if len(sys.argv) > 1:
    for filename in sys.argv[1:]:
      try:
        with open(filename, "rb") as fp:
          sum, blocks = compute_sum(fp.read())
        print(format_sum(sum, blocks), filename)
      except Exception as e:
        print(e)
  else:
    sum, blocks = compute_sum(sys.stdin.buffer.read())
    print(format_sum(sum, blocks))
