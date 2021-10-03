from flask import Blueprint, jsonify, request, abort

from app.models import Dataset

blueprint = Blueprint('views', __name__)

@blueprint.route('/', methods=['GET'])
def hello():
    return jsonify({
        'message': 'App is working.'
    })

@blueprint.route('/angle', methods=['GET'])
def get_solar_angle():
    latitude, longitude = (
        request.args.get('latitude'), 
        request.args.get('longitude')
    )

    if latitude is None or longitude is None:
        abort(400, "Parameter not satisfied.")

    return jsonify(
        Dataset().get_solar_angle(
            parameters=[
                "SG_SAA",
                "SG_SZA"
            ],
            community="RE",
            latitude=latitude,
            longitude=longitude
        )
    )

@blueprint.route('/irradiance', methods=['GET'])
def get_solar_irradiance():
    (
        latitude,
        longitude,
        start,
        end
    ) = (
        request.args.get('latitude'), 
        request.args.get('longitude'),
        request.args.get('start'),
        request.args.get('end')
    )

    if latitude is None or longitude is None or start is None or end is None:
        abort(400, "Parameter not satisfied.")

    return jsonify(
        Dataset().get_solar_irradiance(
            latitude=latitude,
            longitude=longitude,
            start=start,
            end=end
        )
    )

@blueprint.route('/sky', methods=['GET'])
def get_clear_sky_and_amount():
    (
        latitude, 
        longitude, 
        mode,
        start,
        end
    ) = (
        request.args.get('latitude'), 
        request.args.get('longitude'),
        request.args.get('mode'),
        request.args.get('start'),
        request.args.get('end')
    )

    if latitude is None \
        or longitude is None \
            or mode is None \
                or start is None \
                    or end is None:
        abort(400, "Parameter not satisfied.")

    return jsonify(
        Dataset().get_clear_sky_and_amount(
            parameters=[
                "CLRSKY_DAYS",
                "CLOUD_AMT"
            ],
            start=start,
            end=end,
            mode=mode,
            community="RE",
            latitude=latitude,
            longitude=longitude
        )
    )

@blueprint.route('/average', methods=['GET'])
def get_calculate_average_between_values():
    (
        latitude, 
        longitude,
        start,
        end
    ) = (
        request.args.get('latitude'), 
        request.args.get('longitude'),
        request.args.get('start'),
        request.args.get('end')
    )

    return jsonify(
        Dataset().calculate_average_between_values(
            longitude=longitude,
            latitude=latitude,
            start=start,
            end=end
        )
    )
