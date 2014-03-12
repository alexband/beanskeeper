from nose.tools import *

from fnv1a import get_hash_bugfree as get_hash
#from fnv1a import get_hash

def test_fnv1a():
    for s, h in [
                    ("", 0x811c9dc5),
                    ("a", 0xe40c292c),
                    ("foobar", 0xbf9cf968),
                    ("hello", 0x4f9f2cab),
                    ("\xff\x00\x00\x01", 0xc48fb86d),
                ]:
        yield cmp_hash, s, h

def cmp_hash(s, expected_hash):
    hash = get_hash(s)
    if expected_hash >= 0x80000000:
        # sign convertion
        expected_hash = expected_hash - 0x100000000
    eq_(hash, expected_hash)
