import argparse


def configure_parser():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("source", help="RSS URL", type=str, const=None, nargs="?")
    parser.add_argument("--version", help="Print version info", action='version', version="Version 1.4")
    parser.add_argument("--json", help="Print result as JSON in stdout", action='store_true')
    parser.add_argument("--verbose", help="Output verbose status messages", action='store_true')
    parser.add_argument("--limit", help="Limit news topics if this parameter is provided", type=int)
    parser.add_argument("--date", help="Sort news for a given date", type=int)
    parser.add_argument("--to-pdf", help="Export result to .pdf file format", action="store_true")
    parser.add_argument("--to-fb2", help="Export result to .fb2 file format", action="store_true")
    return parser.parse_args()
