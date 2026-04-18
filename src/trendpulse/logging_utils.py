import json
import logging
import sys
import uuid
from typing import Any


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": getattr(record, "trace_id", "-"),
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data)


def setup_logging(level: str = "INFO", json_format: bool = False) -> None:
    log_level = getattr(logging, level.upper(), logging.INFO)

    if json_format:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
    else:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s [%(name)s] [trace_id=%(trace_id)s] %(message)s")
        )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


class TraceAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = kwargs.setdefault("extra", {})
        adapter_extra = self.extra or {}
        extra.setdefault("trace_id", adapter_extra.get("trace_id", str(uuid.uuid4())))
        return msg, kwargs


def get_logger(name: str, trace_id: str | None = None) -> TraceAdapter:
    return TraceAdapter(logging.getLogger(name), {"trace_id": trace_id or str(uuid.uuid4())})
