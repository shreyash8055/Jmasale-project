"""
Celery tasks for the orders app.

Designed to work even when Celery is not installed, so that Django
management commands (check, migrate, etc.) don't crash.
"""

try:
    from celery import shared_task  # type: ignore
except Exception:  # Celery not installed
    def shared_task(func):
        # Fallback: return the original function; mimic .delay by calling directly.
        def delay(*args, **kwargs):
            return func(*args, **kwargs)

        func.delay = delay  # type: ignore[attr-defined]
        return func


@shared_task
def send_order_confirmation(user_email: str) -> None:
    # In real deployment this would send an email; for now we just log/print.
    print(f"Email sent to {user_email}")