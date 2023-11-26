from stravalib.client import Client
from api.auth import schema

# check that.


class StravaClientMixin:
    def get_strava_client(self, user):
        strava = user.social_auth.get(provider='strava')
        return Client(access_token=strava.tokens)
