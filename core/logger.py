import inspect
import logging
import requests
from django.conf import settings
from rest_framework.request import Request


def get_arg_from_stack(arg_type):
    frame = inspect.currentframe()
    while frame := frame.f_back:
        for value in frame.f_locals.values():
            if isinstance(value, arg_type):
                return value

    return None


class Logger:
    _CRITICAL = "critical"
    _ERROR = "error"
    _WARNING = "warning"
    _INFO = "info"
    _DEBUG = "debug"

    def __init__(self, name: str):
        self.name = name
        request = get_arg_from_stack(Request)

        if request is None:
            self.user_id = None
            return

        self.user_id = request.query_params.get("user_id", None) or request.data.get("user_id", None)
        self.user_id = int(self.user_id) if self.user_id else None

    def _network_log(self, level: str, args: tuple, kwargs: dict):
        if not settings.LOG_BASE_URL:
            return

        # Prepare log payload
        data = {
            "args": args,
            "kwargs": kwargs,
        }

        payload = {
            "name": self.name,
            "data": data,
            "value": kwargs.get("value", None),
            "level": level,
            "related_user_id": self.user_id,
            "vertical": settings.VERTICAL,
        }

        try:
            response = requests.post(settings.LOG_BASE_URL, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Ignore all logging errors, do not let them affect main flow
            logging.debug(f"Network log failed for {self.name}: {e}")
            pass

    def _format(self, message: str, args: tuple, kwargs: dict) -> str:
        log = f"{self.name} - UID:{self.user_id} - {message} "
        if args:
            log += f" ".join([str(arg) for arg in args])

        if kwargs:
            log += f" - {kwargs}"

        return log

    def d(self, message: str = "", *args, **kwargs):
        logging.log(logging.DEBUG, self._format(message, args, kwargs))

    def i(self, message: str = "", *args, **kwargs):
        logging.log(logging.INFO, self._format(message, args, kwargs))

    def i_network(self, *args, **kwargs):
        self._network_log(self._INFO, args, kwargs)

    def w(self, message: str = "", *args, **kwargs):
        logging.log(logging.WARNING, self._format(message, args, kwargs))
        self._network_log(self._WARNING, args, kwargs)

    def e(self, message: str = "", *args, **kwargs):
        logging.log(logging.ERROR, self._format(message, args, kwargs))
        self._network_log(self._ERROR, args, kwargs)

    def c(self, message: str = "", *args, **kwargs):
        logging.log(logging.CRITICAL, self._format(message, args, kwargs))
        self._network_log(self._CRITICAL, args, kwargs)
