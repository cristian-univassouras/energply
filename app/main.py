from fastapi import FastAPI
from app.routes import energply

app = FastAPI(title="Enegiply")

app.include_router(energply.router)