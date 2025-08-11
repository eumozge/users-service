import logging
import traceback
from typing import Any
from uuid import UUID

import orjson

logger = logging.getLogger(__name__)


def additionally_serialize(obj: object) -> Any:
    if isinstance(obj, UUID):
        return str(obj)

    logger.warning("Type is not JSON serializable: %s", type(obj), extra={"obj": repr(obj)})
    return repr(obj)


class OrjsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """TODO Configurate request id on api layer."""
        from presentation.api.middlewares.jsonlog import get_request_id

        payload = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": get_request_id(),
        }

        last_frame = self.get_last_frame(record)
        if last_frame:
            payload["traceback"] = last_frame

        return orjson.dumps(payload, default=additionally_serialize).decode()

    def get_last_frame(self, record: logging.LogRecord) -> str | None:
        if not record.exc_info:
            return None

        exc_type, exc_value, exc_traceback = record.exc_info
        if not (exc_type and exc_value and exc_traceback):
            return None

        frames = traceback.format_exception(exc_type, exc_value, exc_traceback)
        return frames[-1].strip() if frames else ""
