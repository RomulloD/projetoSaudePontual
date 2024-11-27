from fastapi import APIRouter
from prisma.errors import UniqueViolationError
from prisma.errors import FieldNotFoundError
from datetime import datetime, timedelta
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from utils.utils import create_access_token
from prismadb import prisma
from models.user import User
from utils.utils import encrypt_password
from utils.utils import check_password
from utils.utils import validate_token
from utils.utils import fuzzy_match
from models.tratamento import Tratamento
from models.tratamento2 import Tratamento2

router = APIRouter(prefix='/med')

@router.get('/get_all_meds')
async def get_all_meds(request: Request):
    try:
        token = validate_token(request.headers)
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Voce nao tem permissao para isso.",
            )
        else:
            try:
                decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
                print(decoded_token)
                print(f"Token é válido! Decodificado: {decoded_token}")
            except ExpiredSignatureError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Voce nao tem permissao para isso.",
                )
            else:
                return await prisma.medicamento.find_many()

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro durante a busca dos medicamentos.",
        )

@router.post('/buscar_medicamento')
async def buscar_medicamento(request: Request, tratamento: Tratamento):
    try:
        token = validate_token(request.headers)
        if token is None:
            print("Token não encontrado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Voce nao tem permissao para isso.",
            )
        else:
            try:
                decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
                print(decoded_token)
                print(f"Token é válido! Decodificado: {decoded_token}")
                print(decoded_token["sub"])
                email = decoded_token["sub"]
                user = await prisma.user.find_unique(where={"email": email})
                search_meds = tratamento.nome.lower()
                medicamento = await prisma.medicamento.find_many()
                #similarity_threshold = 100
                # print(medicamento)
                # print(search_meds)
                resultado = []
                for meds in medicamento:
                    nome_medicamento = meds.nome_produto.lower() if meds.nome_produto.lower else ""
                    meds_similarity = fuzzy_match(search_meds, nome_medicamento)
                    #print (meds_similarity)
                    if meds_similarity > 80:
                        resultado.append({"medicamento": meds})
                print(resultado)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuário não encontrado",
                    )
                print(user)
                print(tratamento)
                return {"results": resultado}
            except ExpiredSignatureError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Voce nao tem permissao para isso.",
                )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro durante a busca dos medicamentos.",
        )
    
@router.post('/registrar_tratamento')
async def registrar_tratamento(request: Request, tratamento: Tratamento2):
    try:
        token = validate_token(request.headers)
        if token is None:
            print("Token não encontrado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Você não tem permissão para isso.",
            )
        else:
            try:
                decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
                print(decoded_token)
                print(f"Token é válido! Decodificado: {decoded_token}")
                print(decoded_token["sub"])
                email = decoded_token["sub"]
                user = await prisma.user.find_unique(where={"email": email})
                print(user)
                print(tratamento)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuário não encontrado",
                    )
                
                tratamento_data = tratamento.dict()
                tratamento_data['user_id'] = user.id

                if 'data_inicio' not in tratamento_data or tratamento_data['data_inicio'] is None:
                    tratamento_data['data_inicio'] = datetime.now()

                if 'id' in tratamento_data:
                    del tratamento_data['id']

                return await prisma.tratamento.create(data=tratamento_data)
            except ExpiredSignatureError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Você não tem permissão para isso.",
                )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro durante o registro do tratamento.",
        )