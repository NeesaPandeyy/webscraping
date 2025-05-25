from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class APIRootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response(
            {
                "accounts": reverse("api-accounts", request=request, format=format),
                "scraper": reverse("api-scraper", request=request, format=format),
                "news": reverse("api-news", request=request, format=format),
                "notification": reverse(
                    "api-notification", request=request, format=format
                ),
            }
        )
