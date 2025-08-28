import sys
import threading
import colorize

_lock = threading.Lock()

def _log(prefix, color, message, bold=False):
    with _lock:
        for line in message.splitlines() or ['']:
            print(colorize.colored(f"{prefix} {line}", color, bold), file=sys.stdout)

def log_success(message):
    _log("[SUCCESS]", colorize.BRIGHT_GREEN, message, bold=True)

def log_warning(message):
    _log("[WARNING]", colorize.BRIGHT_YELLOW, message, bold=True)

def log_error(message):
    _log("[ERROR]", colorize.BRIGHT_RED, message, bold=True)

def log_rendering_file(filename):
    _log("[RENDER]", colorize.BRIGHT_CYAN, f"Rendering file: {filename}", bold=True)

def log_error_rendering_file(filename, error_message):
    _log("[RENDER ERROR]", colorize.BRIGHT_MAGENTA, f"Error rendering file '{filename}': {error_message}", bold=True)
