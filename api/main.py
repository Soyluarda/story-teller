from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.activities import router as activities_router
from api.auth import router as auth_router
from api.exceptions.exception import BaseException
from api.strava import router as strava_router
from api.utils.database import database

app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redocs",
    title="StoryTeller API",
    description="StoryTeller API using FastAPI",
    version="1.0",
    openapi_url="/api/v1/openapi.json",
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.exception_handler(BaseException)
async def unicorn_exception_handler(request: Request, e: BaseException):
    return JSONResponse(status_code=e.status_code, content={"message": e.detail})


app.include_router(auth_router.router, tags=["Auth"])
app.include_router(strava_router.router, tags=["Strava"])
app.include_router(activities_router.router, tags=["Activities"])
