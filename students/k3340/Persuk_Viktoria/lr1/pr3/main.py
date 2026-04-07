from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from typing import List
from typing_extensions import TypedDict
from sqlmodel import select

from models import Warrior, WarriorDefault, Profession, ProfessionDefault, WarriorProfessions, Skill, SkillDefault, WarriorWithSkills
from connection import get_session, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

temp_bd = [
{
    "id": 1,
    "race": "director",
    "name": "Мартынов Дмитрий",
    "level": 12,
    "profession": {
        "id": 1,
        "title": "Влиятельный человек",
        "description": "Эксперт по всем вопросам"
    },
    "skills":
        [{
            "id": 1,
            "name": "Купле-продажа компрессоров",
            "description": ""

        },
        {
            "id": 2,
            "name": "Оценка имущества",
            "description": ""

        }]
},
{
    "id": 2,
    "race": "worker",
    "name": "Андрей Косякин",
    "level": 12,
    "profession": {
        "id": 1,
        "title": "Дельфист-гребец",
        "description": "Уважаемый сотрудник"
    },
    "skills": []
},
]

@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    return session.exec(select(Warrior)).all()


@app.get("/warrior/{warrior_id}", response_model=WarriorWithSkills)
def warriors_get(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)

    if not warrior:
        raise HTTPException(status_code=404, detail='Warrior not found')

    return warrior


@app.post("/warrior")
def warriors_create(
    warrior: Warrior,
    session=Depends(get_session),
    ) -> TypedDict('Response', {"status": int, "data": Warrior}): # type: ignore

    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)

    return {"status": 200, "data": warrior}


@app.delete("/warrior/{warrior_id}")
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)

    if not warrior:
        raise HTTPException(status_code=404, detail='Warrior not found')

    session.delete(warrior)
    session.commit()

    return {'ok': True}


@app.patch("/warrior/{warrior_id}")
def warrior_update(
    warrior_id: int,
    warrior: Warrior,
    session=Depends(get_session),
) -> WarriorDefault:

    db_warrior = session.get(Warrior, warrior_id)

    if not db_warrior:
        raise HTTPException(status_code=404, detail='Warrior not found')

    warrior_data = warrior.model_dump(exclude_unset=True)
    for key, value in warrior_data.items():
        setattr(db_warrior, key, value)

    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)

    return db_warrior


@app.post('/warrior/{warrior_id}/skills/{skill_id}')
def add_skill_to_warrior(
    warrior_id: int,
    skill_id: int,
    session=Depends(get_session)
) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore

    warrior = session.get(Warrior, warrior_id)
    skill = session.get(Skill, skill_id)

    if not warrior or not skill:
        raise HTTPException(status_code=404, detail='Warrior or Skill not found')

    warrior.skills.append(skill)

    session.add(warrior)
    session.commit()

    return {"status": 200, "message": 'skill added'}


@app.delete('warrior/{warrior_id}/skills/{skill_id}')
def remove_skill_from_warrior(
    warrior_id: int,
    skill_id: int,
    session=Depends(get_session)
) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore

    warrior = session.get(Warrior, warrior_id)

    if not warrior:
        raise HTTPException(status_code=404, detail='Warrior not found')

    warrior.skills = [s for s in warrior.skills if s.id != skill_id]

    session.add(warrior)
    session.commit()

    return {"status": 200, "message": 'skill removed'}


@app.get('/warrior/{warrior_id}/skills')
def get_warrior_skills(warrior_id: int, session=Depends(get_session)) -> Skill:
    warrior = session.get(Warrior, warrior_id)

    if not warrior:
        raise HTTPException(status_code=404, detail='Warrior not found')

    return warrior.skills


@app.get('/profession_list')
def profession_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get('/profession/{professions_id}')
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)


@app.post('/profession')
def profession_create(
    prof: ProfessionDefault,
    session=Depends(get_session)
) -> TypedDict('Response', {"status": int, "data": Profession}): # type: ignore

    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)

    return {"status": 200, "data": prof}


@app.get('/skill_list')
def skill_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.get('/skill/{skill_id}')
def skill_get(skill_id: int, session=Depends(get_session)) -> Skill:
    return session.exec(select(Skill).where(Skill.id == skill_id)).first()


@app.post('/skill')
def skill_create(
    skill: SkillDefault,
    session=Depends(get_session)
) -> TypedDict('Response', {'status': int, 'data': Skill}): # type: ignore

    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)

    return {'status': 200, 'data': skill}
