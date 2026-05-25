from datetime import date
from typing import Optional

from pydantic import BaseModel


class ReportFilter(BaseModel):
    """Query parameters for filtering reports by date range

    Attributes:
        date_from: Start date of the report period (inclusive)
        date_to: End date of the report period (inclusive)
    """
    date_from: Optional[date] = None
    date_to: Optional[date] = None


class ReportSummary(BaseModel):
    """Schema for income/expense summary report

    Attributes:
        total_income: Total income amount for the period
        total_expense: Total expense amount for the period
    """
    total_income: float
    total_expense: float


class CategoryReport(BaseModel):
    """Schema for spending breakdown by category

    Attributes:
        category_name: Name of the category
        total_amount: Total amount allocated to this category
    """
    category_name: str
    total_amount: float
