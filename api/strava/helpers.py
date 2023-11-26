import time

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from starlette.config import Config
from stravalib.client import Client

from api.strava import strava_credentials as strava

conf = Config(".env")
client = Client()
chat_model: ChatOpenAI = ChatOpenAI(
    openai_api_key=conf("OPENAI_API_KEY"),
)


def check_token():
    if time.time() > client.token_expires_at:
        refresh_response = client.refresh_access_token(
            client_id=strava.CLIENT_ID,
            client_secret=strava.CLIENT_SECRET,
            refresh_token=client.refresh_token,
        )
        access_token = refresh_response["access_token"]
        refresh_token = refresh_response["refresh_token"]
        expires_at = refresh_response["expires_at"]
        client.access_token = access_token
        client.refresh_token = refresh_token
        client.token_expires_at = expires_at

    return client.access_token


def generate_story(
    distance: str, moving_time: str, total_elevation_gain: str, average_speed: str
):
    story: dict = chat_model.predict_messages(
        [
            HumanMessage(
                content=f"distance: {distance}, moving_time:{moving_time}, "
                f"total_elevation_gain{total_elevation_gain}, average speed{average_speed}"
            ),
            SystemMessage(
                content="Generate a activity story with given these words, keep your responses equals 50 words.",
            ),
        ]
    )
    return story


def generate_title(story: str):
    title: dict = chat_model.predict_messages(
        [
            HumanMessage(
                content=f"{story}",
            ),
            SystemMessage(
                content="Generate a title for the story with given these words, keep your responses equals 10 words.",
            ),
        ]
    )
    return title
