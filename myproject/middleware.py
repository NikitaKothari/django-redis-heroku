import time
import ipaddress
from structlog import get_logger


log = get_logger()


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # trusted_hops_str is the list of IP addresses that Heroku router sees and stores it into x-forwarded-for.
        # x-forwarded-for is a stack and when the Heroku router receives a request, each hop pushes a new IP address onto the end of the stack.
        # As we are using private spaces we don't need to worry about untrusted x-forwarded-for headers and we can trust that the
        # last hop is the client and the corresponding IP is client IP
        log.info(x_forwarded_for)
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    log.info("****************")
    log.info("ip")
    log.info(ip)
    log.info("****************")
    return ip


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
            "ip": get_ip(request),
            "host": request.get_host(),
        }
