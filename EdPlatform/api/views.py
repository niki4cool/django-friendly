from rest_framework.views import APIView
from rest_framework.response import Response

class TestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        data = [{"id": 1, "subject": "english"},{"id": 2,"subject": "math"}]
        return Response(data)
