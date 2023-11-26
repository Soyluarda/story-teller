from langchain.chat_models import ChatOpenAI
from starlette.config import Config

conf = Config(".env")

chat_model: ChatOpenAI = ChatOpenAI(
    openai_api_key=conf("OPENAI_API_KEY"),
)
SITE_URL = conf("SITE_URL")
CLIENT_ID = conf("STRAVA_CLIENT_ID")
CLIENT_SECRET = conf("STRAVA_CLIENT_TOKEN")
REDIRECT_URI = "http://localhost:8000/api/v1/callback"

AUTH_URL = "https://www.strava.com/oauth/authorize"
TOKEN_URL = "https://www.strava.com/oauth/token"

STRAVA_URL = "https://www.strava.com"
AUTHORIZE_URL = f"{STRAVA_URL}/oauth/authorize"
TOKEN_URL = f"{STRAVA_URL}/oauth/token"
ACTIVITIES_URL = f"{STRAVA_URL}/api/v3/athlete/activities"
REDIRECT_URL = f"{SITE_URL}/api/v1/strava/callback/"
