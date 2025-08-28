import config
import colorize
import sys

HELP_TEXT = f"""
{colorize.colored(config.APP, colorize.BRIGHT_GREEN, bold=True)} — Robust tool for building and serving files with dynamic URLs
{colorize.colored("Version", colorize.BRIGHT_RED, bold=True)} {config.VERSION}

{colorize.colored('Commands:', colorize.BRIGHT_CYAN, bold=True)}

  {colorize.colored('build', colorize.BRIGHT_YELLOW, bold=True)}
    {colorize.colored('Process files by injecting the configured base URL', colorize.RESET, bold=True)}
    {colorize.colored('input folder        Source directory containing files to process', colorize.RESET, bold=True)}

    {colorize.colored('Options:', colorize.RESET, bold=True)}
      {colorize.colored('-o, --output folder   Destination directory for processed files (default: out)', colorize.RESET, bold=True)}

  {colorize.colored('serve', colorize.BRIGHT_YELLOW, bold=True)}
    {colorize.colored('Serve files locally', colorize.RESET, bold=True)}
    {colorize.colored('input folder        Source directory containing files to serve', colorize.RESET, bold=True)}

  {colorize.colored('stop', colorize.BRIGHT_YELLOW, bold=True)}
    {colorize.colored('Stop local serve', colorize.RESET, bold=True)}
"""

def Show():
    print(HELP_TEXT)
    sys.exit(0)
