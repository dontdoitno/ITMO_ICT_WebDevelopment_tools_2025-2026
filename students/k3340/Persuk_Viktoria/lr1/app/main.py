from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import auth, user, transaction, wallet


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(wallet.router)
app.include_router(transaction.router)
