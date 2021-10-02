from flask import Blueprint, jsonify, request, abort

from app.models import Dataset

blueprint = Blueprint('views', __name__)

@blueprint.route('/', methods=['GET'])
def hello():
    return jsonify({
        'message': 'App is working.'
    })

@blueprint.route('/solar/angle', methods=['GET'])
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
