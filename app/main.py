from fastapi import FastAPI

from app.routes.users import user_router

app = FastAPI()

app.include_router(user_router)


@app.get("/")
async def index():
    return {"msg": "Hello World!"}
