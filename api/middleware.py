# middleware.py

from django.shortcuts import render

class CustomErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Catch any unhandled exceptions and render the error.html template.
        """
        return render(request, 'error.html', status=500)