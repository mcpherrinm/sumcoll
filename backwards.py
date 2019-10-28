#!/usr/bin/env python3
import sys, os, random

import sum

# backwards.py
# Compute the bsd `sum` algorithm in reverse
# Used for computing collisions and modifying
# somewhere in the middle of the file.

def rotate_left_16bit(data: int) -> int:
  """rotate a 16-bit value to the left"""
  return (0xffff & (data << 1)) | (data >> 15)

def backwards_sum(data: bytes, sum: int) -> int:
  """
  Runs the bsd sum value in reverse

  The return value is what the checksum of a prefix
  must have to achieve the given checksum argument
  """
  for byte in reversed(data):
    sum = rotate_left_16bit((sum - byte) & 0xffff)
  return sum

def test():
  """
  Test that backwards sum matches forward sums

  Generates two random arrays, computes the forwards sum of both together, then
  of the prefix.  Compute the backwards sum of the suffix, and make sure it
  matches the prefix sum.
  """
  prefix = os.urandom(random.randint(10, 10000))
  suffix = os.urandom(random.randint(10, 10000))
  totalsum, _ = sum.compute_sum(prefix + suffix)
  prefixsum, _ = sum.compute_sum(prefix)
  back = backwards_sum(suffix, totalsum)
  assert back == prefixsum

if __name__ == "__main__":
  if len(sys.argv) == 2 and sys.argv[1] == "test":
    for _ in range(0, 1000):
      test()
    print("tests passed")
  elif len(sys.argv) != 3:
    print("Usage: backwards.py file checksum")
    print("backwards.py test")
  else:
    with open(sys.argv[1], "rb") as fp:
      print(backwards_sum(fp.read(), int(sys.argv[2])))
