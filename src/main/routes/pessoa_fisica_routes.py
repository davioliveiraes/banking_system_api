from flask import Blueprint, jsonify

pessoa_fisica_route_bp = Blueprint("pessoa_fisica_routes", __name__)


@pessoa_fisica_route_bp.route("/fisica", methods=["GET"])
def listar_pessoa_fisica():
    return jsonify({"Hello": "World"}), 200
