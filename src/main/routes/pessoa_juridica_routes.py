from flask import Blueprint, jsonify, request

from src.errors.error_handler import handle_errors
from src.main.composer.juridica_criar_composer import juridica_criar_composer
from src.main.composer.juridica_listar_composer import juridica_listar_composer
from src.views.http_types.http_request import HttpRequest

pessoa_juridica_route_bp = Blueprint("pessoa_juridica_routes", __name__)


@pessoa_juridica_route_bp.route("/juridica", methods=["POST"])
def criar_pessoa_juridica():
    try:
        view = juridica_criar_composer()
        http_request = HttpRequest(body=request.json)
        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code


@pessoa_juridica_route_bp.route("/juridica", methods=["GET"])
def listar_pessoa_juridica():
    try:
        view = juridica_listar_composer()
        http_request = HttpRequest()
        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code
