from flask import Blueprint, jsonify

blueprint = Blueprint('errors', __name__)


@blueprint.app_errorhandler(400)
def bad_request(error):
    return jsonify(
        {
            "error": {
                "reason": "Bad request",
                "message": error.description,
                "code": 400
            }
        }
    ), 400


@blueprint.app_errorhandler(401)
def unauthorized(error):
    return jsonify(
        {
            "error": {
                "reason": "Unauthorized",
                "message": error.description,
                "code": 401
            }
        }
    ), 401


@blueprint.app_errorhandler(403)
def forbidden(error):
    return jsonify(
        {
            "error": {
                "reason": "Forbidden",
                "message": error.description,
                "code": 403
            }
        }
    ), 403


@blueprint.app_errorhandler(404)
def not_found(error):
    return jsonify(
        {
            "error": {
                "reason": "Not found",
                "message": error.description,
                "code": 404
            }
        }
    ), 404


@blueprint.app_errorhandler(409)
def conflict(error):
    return jsonify(
        {
            "error": {
                "reason": "Conflict",
                "message": error.description,
                "code": 409
            }
        }
    ), 409


@blueprint.app_errorhandler(500)
def internal_error(error):
    return jsonify(
        {
            "error": {
                "reason": "Internal server error",
                "message": error.description,
                "code": 500
            }
        }
    ), 500
