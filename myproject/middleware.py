import time
from structlog import get_logger
from ipware import get_client_ip


log = get_logger()


def get_ip(request):
    client_ip, is_routable = get_client_ip(request, request_header_order=['HTTP_X_FORWARDED_FOR'])
    log.info("client_ip *******")
    log.info(client_ip)
    if client_ip and is_routable:
       return client_ip
    return None

class RequestLoggingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global log

        request._start = time.time()

        ctx = self.request_context(request)

        log = log.new(**ctx)
        log.info("request received")

        response = self.get_response(request)

        extra_info = {}

        if response.status_code >= 400:
            data = getattr(response, "data", {}) or {}
            extra_info["detail"] = data.get("detail", "no-detail-available")

        if hasattr(request, "_start"):
            start = request._start
            elapsed = int((time.time() - start) * 1000)
            extra_info["elapsed"] = "{}ms".format(elapsed)

        log.info("response complete", status=response.status_code, **extra_info)

        return response

    @staticmethod
    def request_context(request):
        return {
            "process_name": "django",
            "request_id": request.META.get("HTTP_X_REQUEST_ID", "None"),
            "ip": get_ip(request),
            "host": request.get_host(),
            "method": request.method,
            "path": request.get_full_path(),
            "ajax": request.is_ajax(),
            "content_length": request.META.get("CONTENT_LENGTH"),
            "content_type": request.META.get("CONTENT_TYPE"),
            "version": 1,
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
            "client": request.META.get("HTTP_HEROKU_CLIENT", "customer"),
            "context": request.META.get("HTTP_HEROKU_CONTEXT", ""),
        }
