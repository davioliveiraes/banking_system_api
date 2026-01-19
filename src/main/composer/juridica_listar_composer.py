from src.controllers.juridica_listar_controller import PessoaJuridicaListarController
from src.models.sqlite.repositories.pessoa_juridica_repository import (
    PessoaJuridicaRepository,
)
from src.models.sqlite.settings.connection import db_connection_handler
from src.views.juridica_listar_views import PessoaJuridicaListaView


def juridica_listar_composer():
    model = PessoaJuridicaRepository(db_connection_handler)
    controller = PessoaJuridicaListarController(model)
    view = PessoaJuridicaListaView(controller)

    return view
