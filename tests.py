
import unittest

from transform_csv import convert_data_coordinates


class TestExtract(unittest.TestCase):
    def test_extract(self):
        pass


class TestTransform(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.list_points = [
            ['Latitude: 30°02′59″S   -30.04982864', 'Longitude: 51°12′05″W   -51.20150245', 'Distance: 2.2959 km  Bearing: 137.352°'],
            ['Latitude: 30°04′03″S   -30.06761588', 'Longitude: 51°14′23″W   -51.23976111', 'Distance: 4.2397 km  Bearing: 210.121°']
        ]

    def test_convert_incomplete_coordinates(self):
        self.list_points.append(
            ['Latitude: 30°04′03″S   ', 'Longitude: 51°14′23″W   -51.23976111', 'Distance: 4.2397 km  Bearing: 210.121°']
        )
        result = convert_data_coordinates(self.list_points)
        expected_result = [{'latitude': -30.04982864, 'longitude': -51.20150245, 'distance_km': 2.2959,
                            'bearing_degrees': 137.352},
                           {'latitude': -30.06761588, 'longitude': -51.23976111, 'distance_km': 4.2397,
                            'bearing_degrees': 210.121}]
        self.assertEqual(expected_result, result)

    def test_convert_coordinates(self):
        result = convert_data_coordinates(self.list_points)
        expected_result = [{'latitude': -30.04982864, 'longitude': -51.20150245, 'distance_km': 2.2959, 'bearing_degrees': 137.352},
                           {'latitude': -30.06761588, 'longitude': -51.23976111, 'distance_km': 4.2397, 'bearing_degrees': 210.121}]
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
