import requests
from allauth.account.models import EmailAddress
from allauth.account.utils import user_display, user_username
from allauth.core.internal.httpkit import default_get_frontend_url
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import (SocialAccount, SocialToken)
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2CallbackView,
                                                          OAuth2LoginView)
from django.conf import settings


class NTOAuth2Adapter(OAuth2Adapter):
    provider_id = "nepsetrend"
    authorize_url = f"{settings.NT_OAUTH_BASE_URL}/oauth/authorize"
    access_token_url = f"{settings.NT_OAUTH_BASE_URL}/oauth/token"
    profile_url = f"{settings.NT_OAUTH_BASE_URL}/api/user"

    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": f"Bearer {token.token}"}
        response = requests.get(self.profile_url, headers=headers, timeout=5)
        response.raise_for_status()
        extra_data = response.json()
        print("User info response from provider:", extra_data)

        return self.get_provider().sociallogin_from_response(request, extra_data)

    def serialize_user(self, user):
        ret = {
            "display": user_display(user),
            "has_usable_password": user.has_usable_password(),
        }
        if user.pk:
            ret["id"] = user.pk
            email = EmailAddress.objects.get_primary_email(user)
            if email:
                ret["email"] = email

        username = user_username(user)
        if username:
            ret["username"] = username
        if user.is_authenticated:
            try:
                social_account = SocialAccount.objects.filter(
                    user=user, provider=self.provider_id
                ).first()
                if social_account:
                    social_token = SocialToken.objects.filter(
                        account=social_account, app__provider=self.provider_id
                    )
                    if social_token:
                        ret["token"] = social_token.token

            except SocialAccount.DoesNotExist:
                pass

            except SocialToken.DoesNotExist:
                pass

            return ret

    def get_frontend_url(self, urlname, **kwargs):
        return default_get_frontend_url(self.request, urlname, **kwargs)


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        return True


oauth2_login = OAuth2LoginView.adapter_view(NTOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(NTOAuth2Adapter)
