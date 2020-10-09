import logging

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from parking_app.lib.validator import validate_get_parking, validate_put_parking


logger = logging.getLogger(__name__)


class ParkingView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        start_arg = request.GET.get('start')
        end_arg = request.GET.get('end')
        if None in [start_arg, end_arg]:
            return JsonResponse(
                    {'error': 'start and end URL parameters missing'},
                    status=400
            )

        try:
            start, end = validate_get_parking(start_arg, end_arg)
        except Exception as e:
            logger.error(f"Failed to validate query string parameters: {e}")
            return JsonResponse(
                    {'error': f'Invalid start/end dates: {e}'},
                    status=400
            )

        return JsonResponse({'rate': 1750})

    def put(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            rates = validate_put_parking(request.body)
        except Exception as e:
            logger.error(f"Failed to request body: {e}")
            return JsonResponse(
                    {'error': f'Invalid JSON in body: {e}'},
                    status=400
            )

        # Return 201 if data has not been set, 200 otherwise
        return HttpResponse('This is PUT request', status=201)


def health(request: HttpRequest) -> HttpResponse:
    return HttpResponse("I'm alive!")
