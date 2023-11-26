from fastapi import APIRouter

from api.activities.models import activities
from api.utils.database import conn

router = APIRouter(
    prefix="/api/v1",
)


@router.get("/activities/")
async def activity_list():
    return conn.execute(activities.select()).fetchall()


@router.get("/activities/{id}")
async def activity_detail(id: str):
    return conn.execute(activities.select().where(activities.c.id == id)).fetchall()
