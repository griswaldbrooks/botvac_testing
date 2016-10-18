from unittest import TestCase

from botvac_tools.lds import Scan


class TestScanObject(TestCase):
    def test_creation(self):
        scan = Scan()
        self.assertTrue(isinstance(scan, Scan))
