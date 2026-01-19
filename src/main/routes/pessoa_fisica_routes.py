from flask import Blueprint, jsonify, request

from src.main.composer.fisica_criar_composer import fisica_criar_composer
from src.main.composer.fisica_listar_composer import fisica_listar_composer
from src.views.http_types.http_request import HttpRequest

pessoa_fisica_route_bp = Blueprint("pessoa_fisica_routes", __name__)


@pessoa_fisica_route_bp.route("/fisica", methods=["POST"])
def criar_pessoa_fisica():
    view = fisica_criar_composer()
    http_request = HttpRequest(body=request.json)
    http_response = view.handle(http_request)
    return jsonify(http_response.body), http_response.status_code


@pessoa_fisica_route_bp.route("/fisica", methods=["GET"])
def listar_pessoa_fisica():
    view = fisica_listar_composer()
    http_request = HttpRequest()
    http_response = view.handle(http_request)
    return jsonify(http_response.body), http_response.status_code
