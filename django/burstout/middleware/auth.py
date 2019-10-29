
def auth_middleware(get_response=None):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print(request)
        #
        response = get_response(request)
        #
        # # Code to be executed for each request/response after
        # # the view is called.
        #
        return response

    return middleware
