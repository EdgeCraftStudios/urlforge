# ANSI escape codes.

RESET = '\033[0m'
BOLD = '\033[1m'

BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_MAGENTA = '\033[95m'

def colored(text, color, bold=False):
    style = BOLD if bold else ""
    return f"{style}{color}{text}{RESET}"
