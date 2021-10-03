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

    """
        Get Solar Angle (Vertical & Horizontal)
    """
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

    """
        Get Solar Irradiance
    """
    def get_solar_irradiance(
        self,
        longitude = "",
        latitude = "",
        start = 2019,
        end = 2020
    ):
        # Solar Irradiance
        api_solar_irradiance = \
            f"/temporal/climatology/point?parameters=SI_EF_TILTED_SURFACE&community=RE&latitude={latitude}&longitude={longitude}&start={start}&end={end}&format=JSON"
        
        # Solar Irradiance
        api_solar_irradiance_response = requests.get(
            self.base_url + api_solar_irradiance,
            verify=True,
            timeout=30.00
        )

        if api_solar_irradiance_response.status_code != 200:
            abort(500, "Solar Irradiance API Failure")

        # Unpack Solar Irridiance
        (
            horizontal, 
            vertical
        ) = (
            api_solar_irradiance_response.json()['properties']['parameter']['SI_EF_TILTED_SURFACE_HORIZONTAL'],
            api_solar_irradiance_response.json()['properties']['parameter']['SI_EF_TILTED_SURFACE_VERTICAL']
        )
        
        # Map responses
        mapped_solar_irradiance_key_value_dict = defaultdict(list)

        for (key, value) in chain(horizontal.items(), vertical.items()):
            mapped_solar_irradiance_key_value_dict[key].append(value)

        mapped_solar_irradiance_key_value_dict = {
            key: {
                "horizontal": value[0],
                "vertical": value[1]
            }
            for (key, value)
            in mapped_solar_irradiance_key_value_dict.items() 
        }

        return {
            **mapped_solar_irradiance_key_value_dict
        }

    """
        Clear Sky & Amount
    """
    def get_clear_sky_and_amount(
        self,
        mode = "climatology",
        parameters = None,
        community = "",
        longitude = "",
        latitude = "",
        start = "2019",
        end = "2020"
    ):
        if parameters is None:
            abort(400, "Invalid param")
        if not isinstance(parameters, typing.Iterable):
            abort(400, "Parameters is not a List")

        # Clear Sky
        api_clear_sky = \
            f"/temporal/{mode}/point?parameters={parameters[0]}&community={community}&latitude={latitude}&longitude={longitude}&start={start}&end={end}&format=JSON"
        # Cloud Amount
        api_sky_amount = \
            f"/temporal/{mode}/point?parameters={parameters[1]}&community={community}&latitude={latitude}&longitude={longitude}&start={start}&end={end}&format=JSON"
        
        # Clear Sky
        api_clear_sky_response = requests.get(
            self.base_url + api_clear_sky,
            verify=True,
            timeout=30.00
        )
        # Cloud Amount
        api_sky_amount_response = requests.get(
            self.base_url + api_sky_amount,
            verify=True,
            timeout=30.00
        )

        if api_clear_sky_response.status_code != 200:
            abort(500, "Clear Sky API Failure")
        if api_sky_amount_response.status_code != 200:
            abort(500, "Sky Amount API Failure")

        # Unpack Clear Sky and Amount
        (
            clear_sky,
            sky_amount
        ) = (
            api_clear_sky_response.json()['properties']['parameter']['CLRSKY_DAYS'],
            api_sky_amount_response.json()['properties']['parameter']['CLOUD_AMT']
        )

        # Map responses
        mapped_clear_sky_amount_key_value_dict = defaultdict(list)

        for (key, value) in chain(clear_sky.items(), sky_amount.items()):
            mapped_clear_sky_amount_key_value_dict[key].append(value)

        mapped_clear_sky_key_value_dict = {
            key: {
                "clear_sky": value[0],
                "cloud_amount": value[1]
            }
            for (key, value)
            in mapped_clear_sky_amount_key_value_dict.items()
        }

        return {
            **mapped_clear_sky_key_value_dict
        }

    """
        Calculate Average
    """
    def calculate_average_between_values(
        self,
        longitude = "",
        latitude = "",
        start = "2019",
        end = "2020"
    ):
        """
            Function used to calculate average solar irradiance
        """
        def _calculate_average_solar_irradiance():
            # Solar Irradiance
            api_solar_irradiance = \
                f"/temporal/climatology/point?parameters=SI_EF_TILTED_SURFACE&community=RE&latitude={latitude}&longitude={longitude}&format=JSON"

            api_solar_irradiance_response = requests.get(
                self.base_url + api_solar_irradiance,
                verify=True,
                timeout=30.00
            )

            if api_solar_irradiance_response.status_code != 200:
                abort(500, "Solar Irradiance API Failure")

            # Unpack Solar Irridiance
            horizontal, vertical = (
                api_solar_irradiance_response.json()['properties']['parameter']['SI_EF_TILTED_SURFACE_HORIZONTAL'],
                api_solar_irradiance_response.json()['properties']['parameter']['SI_EF_TILTED_SURFACE_VERTICAL']
            )

            # Map & Perform Calculation
            mapped_key_value_dict = defaultdict(list)

            for (key, value) in chain(horizontal.items(), vertical.items()):
                if key != 'ANN':
                    mapped_key_value_dict[key].append(value)

            mapped_key_value_dict = {
                key: (value[0] + value[1]) / 2 # Horizontal + Vertical
                for (key, value)
                in mapped_key_value_dict.items()
            }
            
            return (
                sum(mapped_key_value_dict.values()) / (
                    (int(end) - int(start)) * len(mapped_key_value_dict.items()) - 1 # 12 
                )
            )

        """
            Function used to calculate average clear sky
        """
        def _calculate_average_clear_sky():
            # Clear Sky Daily, Monthly & Climatology
            api_clear_sky_daily = \
                f"/temporal/daily/point?parameters=CLRSKY_DAYS&community=RE&latitude={latitude}&longitude={longitude}&start={start}&end={end}&format=JSON"
            api_clear_sky_monthly = \
                f"/temporal/monthly/point?parameters=CLRSKY_DAYS&community=RE&latitude={latitude}&longitude={longitude}&start={start}&end={end}&format=JSON"
            api_clear_sky_climatology = \
                f"/temporal/climatology/point?parameters=CLRSKY_DAYS&community=RE&latitude={latitude}&longitude={longitude}&start={start}&end={end}&format=JSON"

            api_clear_sky_daily_response = requests.get(
                self.base_url + api_clear_sky_daily,
                verify=True,
                timeout=30.00
            )
            api_clear_sky_monthly_response = requests.get(
                self.base_url + api_clear_sky_monthly,
                verify=True,
                timeout=30.00
            )
            api_clear_sky_climatology_response = requests.get(
                self.base_url + api_clear_sky_climatology,
                verify=True,
                timeout=30.00
            )

            if api_clear_sky_daily_response.status_code != 200:
                abort(500, "Clear Sky Daily API Failure")
            if api_clear_sky_monthly_response.status_code != 200:
                abort(500, "Clear Sky Monthly API Failure")
            if api_clear_sky_climatology_response.status_code != 200:
                abort(500, "Clear Sky Climatology API Failure")

            # Unpack Clear Sky
            (
                clear_sky_daily, 
                clear_sky_monthly, 
                clear_sky_climatology
            ) = (
                api_clear_sky_daily_response.json()['properties']['parameter']['CLRSKY_DAYS'],
                api_clear_sky_monthly_response.json()['properties']['parameter']['CLRSKY_DAYS'],
                api_clear_sky_climatology_response.json()['properties']['parameter']['CLRSKY_DAYS']
            )

            # Map to values
            clear_sky_daily_values = clear_sky_daily.values()
            clear_sky_monthly_values = clear_sky_monthly.values()
            clear_sky_climatology_values = clear_sky_climatology.values()

            # Map & Perform Calculation
            mapped_average_by_category = {
                "daily_average": (
                    sum(clear_sky_daily_values) / (
                        (int(end) - int(start)) * len(clear_sky_daily.keys()) 
                    )
                ),
                "monthly_average": (
                    sum(clear_sky_monthly_values) / (
                        (int(end) - int(start)) * len(clear_sky_monthly.keys()) 
                    )
                ),
                "climatology_average": (
                    sum(clear_sky_climatology_values) / (
                        (int(end) - int(start)) * len(clear_sky_climatology.keys()) 
                    )
                )
            }

            return mapped_average_by_category

        """
            Function used to calculate average cloud amount 
        """
        def _calculate_average_cloud_amount():
            # Cloud Amount
            api_cloud_amount = \
                f"/temporal/monthly/point?parameters=CLOUD_AMT&community=RE&latitude={latitude}&longitude={longitude}&start={start}&end={end}&format=JSON"

            api_cloud_amount_monthly_response = requests.get(
                self.base_url + api_cloud_amount,
                verify=True,
                timeout=30.00
            )

            if api_cloud_amount_monthly_response.status_code != 200:
                abort(500, "Cloud Amount API Failure")

            cloud_amount = api_cloud_amount_monthly_response.json()['properties']['parameter']['CLOUD_AMT']

            # Map to values
            cloud_amount_values = cloud_amount.values()

            return (
                sum(cloud_amount_values) / (
                    (int(end) - int(start)) * len(cloud_amount.keys()) 
                )
            )

        return {
            "average_irradiance": _calculate_average_solar_irradiance(),
            "average_clear_sky": _calculate_average_clear_sky(),
            "average_cloud_amount": _calculate_average_cloud_amount(),
            "total_average": (
                (
                    (_calculate_average_solar_irradiance() * 3.3) + (_calculate_average_clear_sky()['climatology_average'] * 3.3)
                ) - _calculate_average_cloud_amount()
            )
        }