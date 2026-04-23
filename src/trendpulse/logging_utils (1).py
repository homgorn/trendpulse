import logging
import uuid


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] [trace_id=%(trace_id)s] %(message)s",
    )


class TraceAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = kwargs.setdefault("extra", {})
        adapter_extra = self.extra or {}
        extra.setdefault("trace_id", adapter_extra.get("trace_id", "-"))
        return msg, kwargs


def get_logger(name: str, trace_id: str | None = None) -> TraceAdapter:
    return TraceAdapter(logging.getLogger(name), {"trace_id": trace_id or str(uuid.uuid4())})
