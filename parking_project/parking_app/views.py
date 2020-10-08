from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View


class ParkingView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        return JsonResponse({'rate': 1750})

    def post(self, request: HttpRequest, *args, **kwargs):
        return HttpResponse('This is POST request')


def health(request: HttpRequest):
    return HttpResponse("I'm alive!")
