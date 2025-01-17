from fastapi import FastAPI
from routes.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from prismadb import connect_prisma, prisma
import uvicorn
from routes.medicamento import router as medicamento_router

async def lifespan(app: FastAPI):
    await connect_prisma()
    yield
    await prisma.disconnect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(medicamento_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)