from flask import jsonify, make_response

from app import app


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({"error": "Forbidden"}), 403)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request"}), 400)


@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({"error": "Unauthorized"}), 401)


@app.errorhandler(409)
def conflict(error):
    return make_response(jsonify({"error": "Conflict"}), 409)