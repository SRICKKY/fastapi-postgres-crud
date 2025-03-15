from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.users import user_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "https://fastapi-postgres-crud.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)


@app.get("/")
async def index():
    return {"msg": "Hello World!"}
