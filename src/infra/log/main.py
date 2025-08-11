import logging.config

from settings import LogSettings


def configure_logging(settings: LogSettings) -> None:
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(levelname)-8s] %(name)-20s | %(message)s",
            },
            "json": {"()": "infra.log.formatters.OrjsonFormatter"},
        },
        "handlers": {
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "formatter": "json",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "when": "midnight",
                "interval": 1,
                "filename": str(settings.path),
                "backupCount": 14,
            },
        },
        "loggers": {
            "": {"handlers": ["console", "file"], "level": "INFO", "propagate": False},
        },
    }
    logging.config.dictConfig(config)
