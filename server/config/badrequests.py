import falcon
# class HTTP_Request_Error:
#     def __init__(self):
#         super().__init__()
#     def url_not_found(self):
#         if falcon.get_http_status(404) == falcon.HTTP_404:
#             print('yess')
#             return ("Bad Request")
import falcon
class ErrorHandler:
    @staticmethod
    def http(ex, req, resp, params):
        raise ('')

    @staticmethod
    def unexpected(ex, req, resp, params):
        #logger.exception('Unexpected Application Error')
        if falcon.HTTP_404:
            raise('File Not Found')

