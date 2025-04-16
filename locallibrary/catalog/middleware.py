import logging
class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.basicConfig(filename='myapp.log', level=logging.INFO)
        response = self.get_response(request)
        logging.info(f"Log request: {str(request)}")
        logging.info(f"Log response: {str(response)}")
        print(str(request))
        print(str(response)) 
        if request.method=="POST":
            if request.headers=="123":
                print("authenticated user")
        print("logging")
        return response