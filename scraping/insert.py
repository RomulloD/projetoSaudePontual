import orjson
from prisma.errors import UniqueViolationError
from prismadb import prisma
import asyncio


async def insert_medicamento(item):
    medicamento_data = {
        "nome_produto": item.get("NOME_PRODUTO"),
        "numero_registro_produto": item.get("NUMERO_REGISTRO_PRODUTO"),
        "empresa_detentora_registro": item.get("EMPRESA_DETENTORA_REGISTRO"),
        "classe_terapeutica": item.get("CLASSE_TERAPEUTICA", "Desconhecido"),
        "situacao_registro": item.get("SITUACAO_REGISTRO", "Desconhecido")
    }

    try:
        await prisma.medicamento.create(data=medicamento_data)
    except UniqueViolationError:
        print(f"Registro já existe para {medicamento_data['numero_registro_produto']}")
    except Exception as e:
        print(f"Erro ao inserir {medicamento_data['numero_registro_produto']}: {e}")


async def insert_medicamentos_from_json(file_path: str):
    with open(file_path, "rb") as file:
        data = orjson.loads(file.read())

    # Cria uma lista de tarefas assíncronas para inserção com 50 workers
    tasks = []
    for item in data:
        tasks.append(insert_medicamento(item))

    # Limita a execução para 50 tarefas assíncronas simultâneas
    # e aguarda as tarefas terminarem em lotes
    for i in range(0, len(tasks), 50):
        await asyncio.gather(*tasks[i:i + 50])


# Função principal para conectar ao Prisma e iniciar o processo de inserção
async def main():
    await prisma.connect()
    await insert_medicamentos_from_json("dados.json")
    await prisma.disconnect()


# Executa a função principal
asyncio.run(main())
