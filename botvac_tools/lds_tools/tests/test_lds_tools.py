from unittest import TestCase

from botvac_tools.lds_tools.lds_tools import Scan


class TestScanObject(TestCase):
    def test_creation(self):
        scan = Scan()
        self.assertTrue(isinstance(scan, Scan))
