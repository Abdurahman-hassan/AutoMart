from octos.handler.oauth import OAuthHandler
import requests
from django.conf import settings


class OAuthGoogle(OAuthHandler):
    def get_service_url(self):
        return "https://www.googleapis.com/oauth2/v3/userinfo"

    def validate_access_token(self) -> bool:
        validation_url = "https://www.googleapis.com/oauth2/v3/tokeninfo"

        response = requests.get(
            validation_url, params={"access_token": self.access_token}
        )

        if response.status_code == 200:
            token_info = response.json()
            try:
                client_ids = settings.OCTO_OAUTH.get("google")
            except AttributeError:
                raise ValueError(
                    "The 'OCTO_OAUTH' setting is not properly configured. Please ensure 'OCTO_OAUTH' is defined in your settings and contains a valid key for 'google'."
                )
            if token_info["aud"] in client_ids:
                return True

        return False
