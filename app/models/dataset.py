import typing
import requests

from itertools import chain
from collections import defaultdict

from flask import abort

class Dataset:
    def __init__(
        self,
        base_url = "https://power.larc.nasa.gov/api"
    ):
        self.base_url = base_url

    def get_solar_angle(
        self,
        parameters = None,
        community = "",
        longitude = "",
        latitude = ""
    ):
        if parameters is None:
            abort(400, "Invalid param")
        if not isinstance(parameters, typing.Iterable):
            abort(400, "Parameters is not a List")

        api_climatology_azimuth = \
            f"/temporal/climatology/point?parameters={parameters[0]}&community={community}&latitude={latitude}&longitude={longitude}&format=JSON"
        api_climatology_zenith = \
            f"/temporal/climatology/point?parameters={parameters[1]}&community={community}&latitude={latitude}&longitude={longitude}&format=JSON"

        # Horizontal
        api_climatology_azimuth_response = requests.get(
            self.base_url + api_climatology_azimuth,
            verify=True,
            timeout=30.00
        )
        # Vertical
        api_climatology_zenith_response = requests.get(
            self.base_url + api_climatology_zenith,
            verify=True,
            timeout=30.00
        )
        
        if api_climatology_azimuth_response.status_code != 200:
            abort(500, "Azimuth API Failure")
        if api_climatology_zenith_response.status_code != 200:
            abort(500, "Zenith API Failure")

        # Unpack
        (
            horizontal,
            vertical
        ) = (
            api_climatology_azimuth_response.json()['properties']['parameter']['SG_SAA'],
            api_climatology_zenith_response.json()['properties']['parameter']['SG_SZA']
        )

        # Map responses
        mapped_key_value_dict = defaultdict(list)

        for (key, value) in chain(horizontal.items(), vertical.items()):
            mapped_key_value_dict[key].append(value)

        mapped_key_value_dict = {
            key: {
                "vertical": value[0],
                "horizontal": value[1]
            }
            for (key, value)
            in mapped_key_value_dict.items()
        }

        return mapped_key_value_dict