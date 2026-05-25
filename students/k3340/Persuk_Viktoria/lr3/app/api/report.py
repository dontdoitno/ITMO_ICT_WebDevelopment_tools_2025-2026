from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlmodel import select

from auth.utils import get_current_user
from connector import get_session
from models.user import User
from models.transaction import Transaction, TransactionType
from models.transaction_category import TransactionCategory
from models.category import Category
from schemas.report import ReportFilter, CategoryReport, ReportSummary


router = APIRouter(
    prefix='/reports',
    tags=['reports']
)


@router.get('/summary')
def get_summary_report(
    date_filter_query: Annotated[ReportFilter, Query()],
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> ReportSummary:

    query = select(func.sum(Transaction.amount)).where(Transaction.user_id == current_user.id)

    if date_filter_query.date_from:
        query = query.where(Transaction.transaction_date >= date_filter_query.date_from)
    if date_filter_query.date_to:
        query = query.where(Transaction.transaction_date <= date_filter_query.date_to)

    income_transactions = session.exec(query.where(Transaction.type == TransactionType.income)).first()
    if income_transactions is None:
        income_transactions = 0

    expense_transactions = session.exec(query.where(Transaction.type == TransactionType.expense)).first()
    if expense_transactions is None:
        expense_transactions = 0

    return {
        'total_income': income_transactions,
        'total_expense': expense_transactions
    }


@router.get('/by-category')
def get_report_by_category(
    date_filter_query: Annotated[ReportFilter, Query()],
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> List[CategoryReport]:

    report_by_category = []

    query = select(Category.name, func.sum(TransactionCategory.allocated_amount)).join(Category, Category.id == TransactionCategory.category_id).join(Transaction, Transaction.id == TransactionCategory.transaction_id).group_by(Category.name)
    query = query.where(current_user.id == Transaction.user_id)

    if date_filter_query.date_from:
        query = query.where(Transaction.transaction_date >= date_filter_query.date_from)
    if date_filter_query.date_to:
        query = query.where(Transaction.transaction_date <= date_filter_query.date_to)

    reports = session.exec(query).all()

    for report in reports:
        report_by_category.append({
            'category_name': report[0],
            'total_amount': report[1],
        })

    return report_by_category
