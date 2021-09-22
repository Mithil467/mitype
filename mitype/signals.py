"""Custom handlers for received signals."""
import signal
import sys


def exit_on_signal(signum, frame):
    """Exit when SIGINT signal is received."""
    sys.exit(0)


signal.signal(signal.SIGINT, exit_on_signal)
