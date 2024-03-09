# quiz_game/middleware.py

class DebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Middleware - user:", request.user)
        response = self.get_response(request)
        return response
