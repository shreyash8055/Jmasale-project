import time

class APITimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"{request.path} took {execution_time:.4f} seconds")

        return response


