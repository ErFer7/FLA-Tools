'''
Tests for the first list.
'''

import sys
from tests.tests import Tests

if len(sys.argv) < 2:
    print("Usage: python test.py <depth>")
    sys.exit(1)

try:
    DEPTH = int(sys.argv[1])
except ValueError:
    print("Invalid depth.")
    sys.exit(1)

tests = Tests(DEPTH)
tests.run_all()
