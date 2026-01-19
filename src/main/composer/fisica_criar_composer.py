from src.controllers.fisica_criar_controller import PessoaFisicaCriarController
from src.models.sqlite.repositories.pessoa_fisica_repository import (
    PessoaFisicaRepository,
)
from src.models.sqlite.settings.connection import db_connection_handler
from src.views.fisica_criar_views import PessoaFisicaCriarView


def fisica_criar_composer():
    model = PessoaFisicaRepository(db_connection_handler)
    controller = PessoaFisicaCriarController(model)
    view = PessoaFisicaCriarView(controller)

    return view
