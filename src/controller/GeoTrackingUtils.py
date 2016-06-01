import PyQt4
import math


class GeoTrackingUtil(object):
    @staticmethod
    def bearingFromCoordinates(pointA, pointB):

        lat1 = math.radians(pointA['latitude'])
        lat2 = math.radians(pointB['latitude'])
        diffLong = math.radians(pointB['longitude'] - pointA['longitude'])
        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))
        initial_bearing = math.atan2(x, y)

        return (math.degrees(initial_bearing) + 360) % 360

    @staticmethod
    def distanceBetweenCoordinates(pointA, pointB):
        R = 6371
        lat1 = math.radians(pointA['latitude'])
        lat2 = math.radians(pointB['latitude'])
        latDiff = math.radians(pointB['latitude'] - pointA['latitude'])
        longDiff = math.radians(pointB['longitude'] - pointA['longitude'])

        a = math.sin(latDiff / 2) * math.sin(latDiff / 2) + math.cos(lat1) * math.cos(lat2) * math.sin(
                longDiff / 2) * math.sin(longDiff / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
