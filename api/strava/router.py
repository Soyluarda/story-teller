import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from stravalib.client import Client

from api.activities.schema import Activities
from api.strava import strava_credentials as strava
from api.strava.helpers import generate_story, generate_title
from api.utils.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
client = Client()

router = APIRouter(
    prefix="/api/v1",
)


@router.get("/strava/authenticate")
async def strava_authenticate():
    authorize_url = client.authorization_url(
        client_id=strava.CLIENT_ID, redirect_uri=strava.REDIRECT_URL
    )
    return RedirectResponse(url=authorize_url, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/strava/callback/")
def strava_callback(code=None, db: Session = Depends(get_db)):
    token_response = client.exchange_code_for_token(
        client_id=strava.CLIENT_ID, client_secret=strava.CLIENT_SECRET, code=code
    )
    access_token = token_response["access_token"]
    refresh_token = token_response["refresh_token"]
    expires_at = token_response["expires_at"]
    client.access_token = access_token
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{strava.ACTIVITIES_URL}?per_page=3", headers=headers)

    if response.status_code == 200:
        activity_list = []
        for activity in response.json():
            story = generate_story(
                distance=activity["distance"],
                moving_time=activity["moving_time"],
                total_elevation_gain=activity["total_elevation_gain"],
                average_speed=activity["average_speed"],
            )
            title = generate_title(story.content)
            activity_detail = {
                "id": activity["id"],
                "distance": activity["distance"],
                "moving_time": activity["moving_time"],
                "total_elevation_gain": activity["total_elevation_gain"],
                "average_speed": activity["average_speed"],
                "story": story.content,
                "title": title.content,
            }
            activity_list.append(activity_detail)
            existing_activity = (
                db.query(Activities)
                .filter(Activities.id == str(activity["id"]))
                .first()
            )
            if not existing_activity:
                new_activity = Activities(
                    id=activity["id"], title=title.content, story=story.content
                )
                db.add(new_activity)
                db.commit()

        return activity_list
    else:
        raise HTTPException(
            status_code=response.status_code, detail="Unable to fetch activities"
        )
