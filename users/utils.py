from rest_framework.response import Response

def api_response(success, message=None, data=None, status=None):
    response = {
        "success": success,
        "message": message,
        "data": data,
    }
    return Response(response, status=status)
