from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from api.auth import schema
from api.utils import jwt
from stravalib.client import Client
from api.auth.mixins import StravaClientMixin
import requests

chat_model: ChatOpenAI = ChatOpenAI(openai_api_key=config("OPANAI_API_KEY"))

router = APIRouter(
    prefix="/api/v1",
)

@router.get("/user/profile")
async def get_user_profile(current_user: schema.UserList = Depends(jwt.get_current_active_user)):
    return current_user


@router.get("/user/activities")
async def get_user_profile(current_user: schema.UserList = Depends(jwt.get_current_active_user)):
    return current_user

@router.get("/user/strava")
async def get_strava_client(current_user: schema.UserList = Depends(jwt.get_current_active_user)):
    return StravaClientMixin().get_strava_client(user=current_user)


CLIENT_ID = "117253"
CLIENT_SECRET = "8b6996eec5e1c3928c06a8358d9427e4032892cf"
REDIRECT_URI = "http://localhost:8000/api/v1/callback"

# Strava OAuth2 URLs
STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# Callback route after successful authentication
@router.get("/callback")
async def callback(code: str):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(STRAVA_TOKEN_URL, data=data)
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.strava.com/api/v3/athlete/activities?per_page=3", headers=headers)
    return {"data": response.json(), "access_token": access_token}


# Route to fetch user's last 3 activities after authentication
@router.get("/activities")
async def get_activities(): #(token: str = Depends(oauth2_scheme)):
    response = requests.get("https://www.strava.com/api/v3/athlete/activities?per_page=3", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Unable to fetch activities")



client = Client()

def check_token():
    if time.time() > client.token_expires_at:
        refresh_response = client.refresh_access_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, refresh_token=client.refresh_token)
        access_token = refresh_response['access_token']
        refresh_token = refresh_response['refresh_token']
        expires_at = refresh_response['expires_at']
        client.access_token = access_token
        client.refresh_token = refresh_token
        client.token_expires_at = expires_at

REDIRECT_URL = 'http://localhost:8000/api/v1/authorized'

# Route to initiate Strava authentication
@router.get("/strava/authorize")
async def strava_authorize():
    authorize_url = client.authorization_url(client_id=CLIENT_ID, redirect_uri=REDIRECT_URL)
    return RedirectResponse(url=authorize_url, status_code=status.HTTP_303_SEE_OTHER)
    #return {"url": f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=read,activity:read_all"}


@router.get("/authorized/")
def get_code(state=None, code=None, scope=None):
    token_response = client.exchange_code_for_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=code)
    access_token = token_response['access_token']
    refresh_token = token_response['refresh_token']
    expires_at = token_response['expires_at']
    client.access_token = access_token
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.strava.com/api/v3/athlete/activities?per_page=1", headers=headers)

   # prediction_msg: dict = chat_model.predict_messages(
   #     [HumanMessage(content=""),
   #      SystemMessage(
   #          content="Talk like you are a German, keep your responses below 50 words but more than 40 words.")])

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Unable to fetch activities")
    #curr_athlete = client.get_athlete()
   # save_object(client, 'client.pkl')
    return {"state": state, "code": code, "scope": scope, "token_response": token_response}
          #  "curr_athlete": client.get_athlete()}