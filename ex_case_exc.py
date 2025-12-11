"""
exc_type: O tipo de exceção que ocorreu, se houver.
    Se não ocorreu nenhuma exceção, este parâmetro será None

exc_val: O valor de exceção que ocorreu, se houver.
    Se não ocorreu nenhuma exceção, este parâmetro será None

exc_tb: O traceback (rastreamento de pilha) associado à exceção que ocorreu, se h
    Se não ocorreu nenhuma exceção, este parâmetro será None

Exemplo alternativo: Context Manager com tratamento de exceções
Este exemplo demonstra como usar os parâmetros do __exit__ para:
1. Capturar e logar exceções
2. Decidir se suprime ou propaga a exceção
3. Realizar cleanup mesmo quando ocorrem erros

"""


class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        print(f"Abrindo conexão com {self.db_name}")
        self.connection = f"Connection to {self.db_name}"
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Sempre fechar a conexão, mesmo se houver algum erro.
        print(f"Fechando conexão com {self.db_name}")

        # Se houve uma conexão
        if exc_type is not None:
            print("\n ERRO DETECTADO:")
            print(f"  Tipo: {exc_type.__name__}")
            print(f"  Mensagem: {exc_val}")
            print(f"  Linha do erro: {exc_tb.tb_lineno}")

            # Se for ValueErro, suprime o erro (retorna True)
            if exc_type == ValueError:
                print("  Value Error foi tratado e suprimido")
                return True  # Suprime a exceção

            # Outros erros serão propagados (retorna False ou None)
            print("  Exceção será propagada")
            return False

        print("Operação concluída sem erros")
        return None


# Exemplo 1: Sem exceção
print("=" * 50)
print("CASO 1: Operação Normal (sem erros)")
print("=" * 50)
with DatabaseConnection("users.db") as db:
    print(f"Executando query no {db.connection}")
    print("Query executada com sucesso!")

print("\n")

# Exemplo 2: Com ValueError (será suprimido)
print("=" * 50)
print("CASO 2: ValueError (será suprimido)")
print("=" * 50)
try:
    with DatabaseConnection("products.db") as db:
        print(f"Executando query no {db.connection}")
        raise ValueError("Valor inválido no banco de dados")
except ValueError:
    print("Este except não será executado porque o erro foi suprimido!")
print("Programa continua normalmente após ValueError")

print("\n")

# Exemplo 3: Com TypeError (será propagado)
print("=" * 50)
print("CASO 3: TypeError (será propagado)")
print("=" * 50)
try:
    with DatabaseConnection("orders.db") as db:
        print(f"Executando query no {db.connection}")
        raise TypeError("Tipo incompatível")
except TypeError as e:
    print(f"TypeError foi capturado aqui: {e}")
