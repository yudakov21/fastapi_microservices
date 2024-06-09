from fastapi import FastAPI
from app.api.orders import router

app = FastAPI(
    title='Orders'
)

app.include_router(router)

