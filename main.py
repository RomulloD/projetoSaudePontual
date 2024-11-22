from fastapi import FastAPI
from routes.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from prismadb import connect_prisma, prisma
import uvicorn
from routes.medicamento import router as medicamento_router

app = FastAPI()

# Configurações do middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo o roteador de usuário
app.include_router(user_router)
app.include_router(medicamento_router)

# Evento de inicialização do Prisma
@app.on_event("startup")
async def startup_event():
    await connect_prisma()

# Evento de desligamento do Prisma
@app.on_event("shutdown")
async def shutdown_event():
    await prisma.disconnect()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)