import time
import ipaddress
from structlog import get_logger


log = get_logger()


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # IP chains should always be read from left-to-right, The client IP should always be the left-most IP
        ip = x_forwarded_for.split(",")[0]
        log.info("****************")
        log.info("ip")
        log.info(ip)
        log.info("****************")
    else:
        ip = request.META.get("REMOTE_ADDR")

    log.info("------------------------------")
    log.info("HTTP_X_FORWARDED_FOR")
    log.info(request.META.get("HTTP_X_FORWARDED_FOR"))
    log.info("REMOTE_ADDR")
    log.info(request.META.get("REMOTE_ADDR"))
    log.info("------------------------------")

    ipv6 = ipaddress.ip_address("10.5.206.253")
    log.info("****************")
    log.info(ipv6)
    log.info(ipv6.is_private)
    ipv6 = ipaddress.ip_address("13.110.54.38")
    log.info("****************123")
    log.info(ipv6)
    log.info(ipv6.is_private)
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
