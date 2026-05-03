import logging
import os

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

OTEL_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
SERVICE_NAME  = "motor-de-busca"

resource = Resource.create({"service.name": SERVICE_NAME})

_tracer: trace.Tracer = None
_meter:  metrics.Meter = None
_logger: logging.Logger = None

# Metric instruments (populated in setup_telemetry)
search_duration_histogram = None
search_requests_counter   = None
document_size_histogram   = None


def setup_telemetry():
    global _tracer, _meter, _logger
    global search_duration_histogram, search_requests_counter, document_size_histogram

    # ── Traces ──────────────────────────────────────────
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=OTEL_ENDPOINT, insecure=True))
    )
    trace.set_tracer_provider(tracer_provider)
    _tracer = trace.get_tracer(SERVICE_NAME)

    # ── Metrics ─────────────────────────────────────────
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=OTEL_ENDPOINT, insecure=True),
        export_interval_millis=15_000,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    _meter = metrics.get_meter(SERVICE_NAME)

    search_duration_histogram = _meter.create_histogram(
        name="search_duration_ms",
        description="Tempo de execução da busca em milissegundos",
        unit="ms",
    )
    search_requests_counter = _meter.create_counter(
        name="search_requests_total",
        description="Total de buscas realizadas",
    )
    document_size_histogram = _meter.create_histogram(
        name="document_size_chars",
        description="Tamanho do documento em caracteres",
        unit="chars",
    )

    # ── Logs ────────────────────────────────────────────
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter(endpoint=OTEL_ENDPOINT, insecure=True))
    )
    set_logger_provider(logger_provider)

    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().addHandler(handler)

    _logger = logging.getLogger(SERVICE_NAME)


def get_tracer() -> trace.Tracer:
    return _tracer


def get_logger() -> logging.Logger:
    return _logger


def record_search(algorithm: str, found: bool, duration_ms: float, n: int, m: int):
    labels = {"algorithm": algorithm, "found": str(found).lower()}
    search_duration_histogram.record(duration_ms, labels)
    search_requests_counter.add(1, labels)
    document_size_histogram.record(n, {"algorithm": algorithm})
