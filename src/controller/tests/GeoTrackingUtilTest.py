import unittest
from controller.GeoTrackingUtils import GeoTrackingUtil
import math


class GeoTrackingUtilTest(unittest.TestCase):
    DISTANCE_FROM_MONTREAL_TO_TORONTO = 504
    BEARING_FROM_TORONTO_TO_MONTREAL = 63

    def setUp(self):
        self.__montreal = {'latitude': 45.5017, 'longitude': -73.5673}
        self.__quebec = {'latitude': 46.8139, 'longitude': -71.2080}
        self.__toronto = {'latitude': 43.6532, 'longitude': -79.3832}

    def test_bearing_calculation(self):
        self.assertAlmostEqual(math.floor(GeoTrackingUtil.bearingFromCoordinates(self.__toronto, self.__montreal)),
                               self.BEARING_FROM_TORONTO_TO_MONTREAL)

    def test_distance_calculation(self):
        self.assertAlmostEqual(math.floor(GeoTrackingUtil.distanceBetweenCoordinates(self.__montreal, self.__toronto)),
                               self.DISTANCE_FROM_MONTREAL_TO_TORONTO)


if __name__ == "__main__":
    unittest.main()
