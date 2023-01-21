from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse

class TestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        data = [{"id": 1, "subject": "english"},{"id": 2,"subject": "math"}]
        return Response(data)

def test(request):
    return HttpResponse("Hello World")