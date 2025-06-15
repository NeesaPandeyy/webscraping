from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

from .views import NTOAuth2Adapter


class NTOauth2Account(ProviderAccount):
    pass


class NTOauth2Provider(OAuth2Provider):
    id = "nepsetrend"
    name = "Nepsetrend"
    account_class = NTOauth2Account
    oauth2_adapter_class = NTOAuth2Adapter

    def extract_uid(self, data):
        uid = data.get("id")
        if uid is None:
            raise ValueError("No user ID found in OAuth response")
        return str(uid).strip()

    def extract_common_fields(self, data):
        return {
            "email": data.get("email"),
            "first_name": data.get("first_name"),
            "is_active": data.get("active", True),
        }

    def get_default_scope(self):
        return ["*"]


provider_classes = [NTOauth2Provider]
