'''
- [ ] POST /categories — create category
- [ ] GET /categories — list user's categories
- [ ] PATCH /categories/{id} — update category (verify ownership)
- [ ] DELETE /categories/{id} — delete category (verify ownership)
'''
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from auth.utils import get_current_user
from connector import get_session
from models.user import User
from models.category import Category
from schemas.category import CategoryCreate, CategoryRead, CategoryUpdate


router = APIRouter(
    prefix='/categories',
    tags=['categories'],
)


@router.post('/')
def create_category(
    data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> CategoryRead:

    new_category = Category(
        user_id=current_user.id,
        name=data.name,
        type=data.type
    )

    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return new_category


@router.get('/')
def get_categories(
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> List[CategoryRead]:

    categories = session.exec(select(Category).where(Category.user_id == current_user.id)).all()

    return categories


@router.patch('/{id}')
def update_category(
    id: int,
    data: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> CategoryRead:

    category_db = session.exec(select(Category).where(Category.id == id).where(Category.user_id == current_user.id)).first()

    if not category_db:
        raise HTTPException(status_code=404, detail='Category not found')

    if data.name is not None:
        category_db.name = data.name
    if data.type is not None:
        category_db.type = data.type

    session.add(category_db)
    session.commit()
    session.refresh(category_db)

    return category_db


@router.delete('/{id}')
def delete_category(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):

    category_db = session.exec(select(Category).where(Category.id == id).where(Category.user_id == current_user.id)).first()

    if not category_db:
        raise HTTPException(status_code=404, detail='Category not found')

    session.delete(category_db)
    session.commit()

    return {'message': 'category deleted'}
