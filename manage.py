#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PrimeCare_Medical_Institute.settings')
    # On Windows, the console is often cp1252, which can't encode the
    # emoji used in some email bodies (e.g. the console email backend used
    # in demo mode). Force UTF-8 so printing those doesn't crash the server.
    for stream_name in ('stdout', 'stderr'):
        stream = getattr(sys, stream_name)
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8', errors='replace')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
