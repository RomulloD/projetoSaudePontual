import sys
import os
import asyncio
from prisma import Prisma
from prisma.errors import UniqueViolationError
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prismadb import prisma

async def insert_medicamento(item):
    categoria_regulatoria = item.get("CATEGORIA_REGULATORIA")
    if not categoria_regulatoria:
        print(f"Erro: 'CATEGORIA_REGULATORIA' não está definido para {item.get('NUMERO_REGISTRO_PRODUTO')}")
        return

    medicamento_data = {
        "tipo_produto": item.get("TIPO_PRODUTO"),
        "nome_produto": item.get("NOME_PRODUTO"),
        "data_finalizacao_processo": datetime.strptime(item.get("DATA_FINALIZACAO_PROCESSO"), "%d/%m/%Y") if item.get("DATA_FINALIZACAO_PROCESSO") else None,
        "categoria_regulatoria": categoria_regulatoria,
        "numero_registro_produto": item.get("NUMERO_REGISTRO_PRODUTO"),
        "data_vencimento_registro": datetime.strptime(item.get("DATA_VENCIMENTO_REGISTRO"), "%d/%m/%Y") if item.get("DATA_VENCIMENTO_REGISTRO") else None,
        "numero_processo": item.get("NUMERO_PROCESSO"),
        "classe_terapeutica": item.get("CLASSE_TERAPEUTICA"),
        "empresa_detentora_registro": item.get("EMPRESA_DETENTORA_REGISTRO"),
        "situacao_registro": item.get("SITUACAO_REGISTRO"),
        "principio_ativo": item.get("PRINCIPIO_ATIVO")
    }

    try:
        await prisma.medicamento.create(data=medicamento_data)
    except UniqueViolationError:
        print(f"Registro já existe para {medicamento_data['numero_registro_produto']}")
    except Exception as e:
        print(f"Erro ao inserir {medicamento_data['numero_registro_produto']}: {e}")

async def insert_medicamentos_from_json(file_path: str):
    import json
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    tasks = [insert_medicamento(item) for item in data]
    
    # Limita a execução para 50 tarefas assíncronas simultâneas
    # e aguarda as tarefas terminarem em lotes
    for i in range(0, len(tasks), 50):
        await asyncio.gather(*tasks[i:i + 50])

# Função principal para conectar ao Prisma e iniciar o processo de inserção
async def main():
    await prisma.connect()
    await insert_medicamentos_from_json("scraping/dados.json")
    await prisma.disconnect()

# Executa a função principal
asyncio.run(main())