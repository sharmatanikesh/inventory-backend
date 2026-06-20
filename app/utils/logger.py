import logging
import sys
import structlog
from app.config import NewConfig

def setup_logger():
    """Initializes and configures the structlog logging system."""
    config = NewConfig()
    is_local = config.IsLocalEnvironment()
    
    # Use DEBUG level in local/development and INFO in production
    log_level = logging.DEBUG if is_local else logging.INFO
    
    processors = [
        # Merges context-local variables (bound dynamically per request/thread)
        structlog.contextvars.merge_contextvars,
        # Adds 'level' field
        structlog.processors.add_log_level,
        # Adds human-readable timestamp
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=False),
        # Handles exception info extraction and formatting
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        # Pretty console formatter with colors
        structlog.dev.ConsoleRenderer(colors=True)
    ]
    
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=True,
    )

# Expose a default configured logger instance
logger = structlog.get_logger()
