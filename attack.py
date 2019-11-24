#!/usr/bin/env python3

import sys, collections

import sum, backwards

# middle.py
# A meet-in-the-middle attack on the BSD sum algorithm
# We take advantage of the birthday paradox and search for prefix extensions
# and suffix extensions simultanously.

def search(start: int, end: int, charset: bytes) -> bytes:
  """
  Takes a start and end checksum values and a set of characters to use.

  returns the bytestring to insert to cause the desired collision
  """

  prefix_candidates = collections.deque([(b'', start)])
  suffix_candidates = collections.deque([(b'', end)])
  prefix_hashes = {start: b''}
  suffix_hashes = {end: b''}

  while True:
    prefix_base, cksum = prefix_candidates.popleft()

    for c in charset:
      new_sum = sum.add(cksum, c)
      new_prefix = prefix_base + bytes([c])
      suf = suffix_hashes.get(new_sum)
      if suf is not None:
        return new_prefix + suf
      if prefix_hashes.get(new_sum) is None:
        prefix_candidates.append((new_prefix, new_sum))
        prefix_hashes[new_sum] = new_prefix

    suffix_base, cksum = suffix_candidates.popleft()
    for c in charset:
      new_sum = backwards.sub(cksum, c)
      new_suffix = bytes([c]) + suffix_base
      pre = prefix_hashes.get(new_sum)
      if pre is not None:
        return pre + new_suffix
      if suffix_hashes.get(new_sum) is None:
        suffix_candidates.append((new_suffix, new_sum))
        suffix_hashes[new_sum] = new_suffix

if __name__ == "__main__":
  filename = sys.argv[1]
  offset = int(sys.argv[2])

  data = open(filename, 'rb').read()

  start, _ = sum.compute_sum(data[:offset])
  end = backwards.backwards_sum(data[offset:], 0)

  charset = bytes(range(ord(' '), ord('~')+1))
  added = search(start, end, charset)

  print(added)

  out = open(sys.argv[3], 'wb')
  out.write(data[:offset])
  out.write(added)
  out.write(data[offset:])
