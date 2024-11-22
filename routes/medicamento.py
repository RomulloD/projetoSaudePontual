from fastapi import APIRouter
from prisma.errors import UniqueViolationError
from prisma.errors import FieldNotFoundError
from datetime import timedelta
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

