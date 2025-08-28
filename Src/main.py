import sys
import os
import argparse
import logger
import help
import build
import serve

DISALLOWED_ARGS = {'-h', '--h', '-help', '--help'}

def main():
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        sys.exit(0)

    for arg in sys.argv[1:]:
        if arg.lower() in DISALLOWED_ARGS:
            logger.log_error("Invalid help flag. Use 'help' as a command instead.")
            sys.exit(1)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('command', nargs='?', help='Command to run: build, serve, help')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments for the command')

    parsed = parser.parse_args()

    if not parsed.command:
        logger.log_error("No command specified. Use 'help' to see available commands.")
        sys.exit(1)

    cmd = parsed.command.lower()

    if cmd == 'help':
        help.Show()
    elif cmd == 'build':
        build.build(parsed.args)
    elif cmd == 'serve':
        serve.serve(parsed.args)
    else:
        logger.log_error(f"Unknown command '{cmd}'. Use 'help' to see available commands.")
        sys.exit(1)

if __name__ == '__main__':
    main()
