from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)


def setup_tracing() -> None:
    resource = Resource.create(
        {
            "service.name": "enterprise-mcp-gateway",
        }
    )

    provider = TracerProvider(
        resource=resource,
    )

    processor = SimpleSpanProcessor(
        ConsoleSpanExporter()
    )

    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)


tracer = trace.get_tracer(
    "enterprise-mcp-gateway"
)


def trace_tool_execution(
    tool_name: str,
    function,
    *args,
    **kwargs,
):
    with tracer.start_as_current_span(
        f"tool:{tool_name}"
    ) as span:

        span.set_attribute(
            "tool.name",
            tool_name,
        )

        try:
            result = function(
                *args,
                **kwargs,
            )

            span.set_attribute(
                "tool.success",
                True,
            )

            return result

        except Exception as exc:
            span.set_attribute(
                "tool.success",
                False,
            )

            span.record_exception(exc)

            raise