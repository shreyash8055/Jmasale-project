"""
Project package init.

Important: keep this file lightweight so Django can start even when optional
dependencies (like Celery) are not installed.
"""

try:
    # Expose Celery app if Celery is installed and configured.
    from jmasale.celery_app import app as celery_app  # type: ignore

    __all__ = ("celery_app",)
except Exception:
    # Celery is optional for running Django management commands (check/migrate/etc).
    __all__ = ()

