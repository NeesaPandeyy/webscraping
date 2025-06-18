from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class APIRootView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, format=None):
        return Response(
            {
                "accounts": reverse("api-accounts", request=request, format=format),
                "scraper": reverse("api-scraper", request=request, format=format),
                "news": reverse("api-news", request=request, format=format),
                "notification": reverse(
                    "api-notification", request=request, format=format
                ),
                "search": reverse("api-search", request=request, format=format),
            }
        )
