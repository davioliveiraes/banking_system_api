from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = "sqlite:///storage.db"
        self.__engine = None
        self.session = None

    def connect_to_be(self):
        try:
            self.__engine = create_engine(
                self.__connection_string,
                echo=False,
                pool_pre_ping=True,
            )
            with self.__engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(" Conexão com banco estabelecida")
        except Exception as e:
            raise RuntimeError(f"Erro ao conectar ao banco: {e}") from e

    def get_engine(self):
        if self.__engine is None:
            self.connect_to_be()
        return self.__engine

    def __enter__(self):
        if self.__engine is None:
            raise RuntimeError(
                "Engine não inicializado."
                "Chame connect_to_be() antes de usar o context manager."
            )
        try:
            session_maker = sessionmaker(bind=self.__engine)
            self.session = session_maker()
            return self
        except Exception as e:
            raise RuntimeError(f"Erro ao criar sessão: {e}") from e

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Gerencia o fechamento da sessão e tratamento de exceções.
            - Se houve exceção: faz rollback
            - Se não houve exceção: faz commit (opcional, depende do uso)
            - Sempre fecha a sessão
        """
        if self.session is None:
            return False

        try:
            if exc_type is not None:
                print(f" Erro detectado: {exc_type.__name__}: {exc_val}")
                print("  Fazendo rollback da transação...")
                self.session.rollback()
                return False
            # else:
            # self.session.commit()
            # pass
        except Exception as close_error:
            print(f" Erro ao finalizar sessão: {close_error}")
            return False
        finally:
            try:
                self.session.close()
            except Exception as e:
                print(f"  Erro ao fechar sessão: {e}")
        return False


db_connection_handler = DBConnectionHandler()
