from src.controllers.fisica_listar_controller import PessoaFisicaListarController
from src.models.sqlite.repositories.pessoa_fisica_repository import (
    PessoaFisicaRepository,
)
from src.models.sqlite.settings.connection import db_connection_handler
from src.views.fisica_listar_views import PessoaFisicaListarViews


def fisica_listar_composer():
    model = PessoaFisicaRepository(db_connection_handler)
    controller = PessoaFisicaListarController(model)
    view = PessoaFisicaListarViews(controller)

    return view
