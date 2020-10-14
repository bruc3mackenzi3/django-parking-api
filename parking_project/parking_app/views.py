import logging

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View

from parking_app.lib.rates import ParkingRates
from parking_app.lib.validator import validate_get_parking, validate_put_parking


class ParkingQueryView(View):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(ParkingQueryView.__name__)
        super(ParkingQueryView, self).__init__(*args, **kwargs)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not ParkingRates.rates_loaded():
            self.logger.error("Unable to process query, parking rates not yet loaded.")
            return JsonResponse(
                    {"error": "Parking rates not yet loaded"},
                    status=503
            )
        start_arg = request.GET.get("start")
        end_arg = request.GET.get("end")
        if None in [start_arg, end_arg]:
            return JsonResponse(
                    {"error": "start and end URL parameters missing"},
                    status=400
            )

        try:
            start, end = validate_get_parking(start_arg, end_arg)
        except Exception as e:
            self.logger.error(f"Failed to validate query string parameters: {e}")
            return JsonResponse(
                    {"error": f"Invalid start/end dates: {e}"},
                    status=400
            )

        price = ParkingRates.get_rate_price(start, end)

        if price == None:
            price = "unavailable"
        return JsonResponse({"rate": price})


class ParkingRatesView(View):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(ParkingRatesView.__name__)
        super(ParkingRatesView, self).__init__(*args, **kwargs)
    def put(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # Return 201 if data has not been set, 200 otherwise
        if not ParkingRates.rates_loaded():
            return_status = 201
        else:
            return_status = 200

        try:
            rates_dict = validate_put_parking(request.body)
        except Exception as e:
            self.logger.error(f"Failed to load request body: {e}")
            return JsonResponse(
                    {"error": f"Invalid JSON in body: {e}. Parking rates not updated."},
                    status=400
            )

        try:
            ParkingRates.load_rates(rates_dict)
        except Exception as e:
            self.logger.error(f"Error loading rates objects: {e}")
            return JsonResponse(
                    {"error": f"Invalid field in rates: {e}. Parking rates not updated."},
                    status=400
            )

        return HttpResponse("", status=return_status)


def health(request: HttpRequest) -> HttpResponse:
    return HttpResponse("I'm alive!")
