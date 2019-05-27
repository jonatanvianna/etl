


import pandas as pd

# given: lat1, lon1, bearing, distMiles
# lat2, lon2 = VincentyDistance(miles=distMiles).destination(Point(lat1, lon1), bearing)
# lat1, lon1, distMiles, bearing = 42.189275,-76.85823, 0.5, 30

from googlemaps import Client as GoogleMapsClient
from googlemaps.exceptions import ApiError


def get_address_from_coordinates(latitude, longitude):
    """Converts a latitude, longitude address coordinate in a valid address

    :param latitude: float
    :param longitude: float
    :return: dict
    """
    maps = GoogleMapsClient(key="AIzaSyCZ1RwYvtM-fbjWp7ZQnMggAVJVS9LJMFA")



    try:
        return self.maps.reverse_geocode(
            (latitude, longitude),
            result_type="street_address",
            location_type="ROOFTOP",
        )
    except ApiError as e:
        logger.critical(e.message)
        os.sys.exit(1)





        # result = self.get_address_from_coordinates(
        #     coordinate["latitude"], coordinate["longitude"]
        # )
        # if result:
        #     address_components = result[0].get("address_components", "")
        #     if address_components:
        #         complete_address = self.get_address_from_address_components(
        #             address_components
        #         )
        #         if complete_address:
        #             complete_address.update(
        #                 {
        #                     "latitude": coordinate["latitude"],
        #                     "longitude": coordinate["longitude"],
        #                 }
        #             )
        #             if self.is_address_valid(complete_address):
        #                 logger.info(
        #                     f"Address saved to database: {complete_address}"
        #                 )
        #                 coordinate = {
        #                     "latitude": coordinate["latitude"],
        #                     "longitude": coordinate["longitude"],
        #                     "distance_km": coordinate["distance_km"],
        #                     "bearing_degrees": coordinate["bearing_degrees"],
        #                 }

        #                 addresses = {
        #                     "street_number": complete_address.get("street_number"),
        #                     "street_name": complete_address.get("street_name"),
        #                     "neighborhood": complete_address.get("neighborhood"),
        #                     "city": complete_address.get("city"),
        #                     "state": complete_address.get("state"),
        #                     "country": complete_address.get("country"),
        #                     "postal_code": complete_address.get("postal_code"),
        #                     "latitude": complete_address.get("latitude"),
        #                     "longitude": complete_address.get("longitude"),
        #                 }

        #                 self.save_to_database(coordinate, addresses)
        # else:
        #     logger.warning(
        #         f"Address couldn't be saved to database. Data returned from reverse_geocode API: {result}"
        #     )


if __name__ == "__main__":
    save_dataset_coordinates_to_database()
