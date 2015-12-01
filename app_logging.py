import logging

_log = None


def get_logger():
    global _log
    if _log is None:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        _log = logging.getLogger("werkzeug")
        _log.addHandler(console_handler)
        _log.setLevel(logging.DEBUG)
        _log.debug("Logger set")

    return _log
