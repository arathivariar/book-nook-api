from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to Book Nook, a community for bibliophiles. At Book Nook, we love reading!"
    })