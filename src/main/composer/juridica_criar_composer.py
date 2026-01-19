from src.controllers.juridica_criar_controller import PessoaJuridicaCriarControler
from src.models.sqlite.repositories.pessoa_juridica_repository import (
    PessoaJuridicaRepository,
)
from src.models.sqlite.settings.connection import db_connection_handler
from src.views.juridica_criar_views import PessoaJuridicaCriarViews


def juridica_criar_composer():
    model = PessoaJuridicaRepository(db_connection_handler)
    controller = PessoaJuridicaCriarControler(model)
    view = PessoaJuridicaCriarViews(controller)

    return view
