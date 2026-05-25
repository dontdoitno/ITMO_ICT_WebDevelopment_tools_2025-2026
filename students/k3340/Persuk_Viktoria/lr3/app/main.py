from contextlib import asynccontextmanager

from fastapi import FastAPI

from connector import init_db
from api import auth, user, transaction, wallet, budget, category, goal, notification, report, transaction_category, goal_transaction, parse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(wallet.router)
app.include_router(transaction.router)
app.include_router(budget.router)
app.include_router(category.router)
app.include_router(goal.router)
app.include_router(transaction_category.router)
app.include_router(goal_transaction.router)
app.include_router(notification.router)
app.include_router(report.router)
app.include_router(parse.router)
