from parser_engine import Parser
import argparse

parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
parser.add_argument("source", help="RSS URL", type=str)
parser.add_argument("--version", help="Print version info", action='version', version="Version 1.5")
parser.add_argument("--json", help="Print result as JSON in stdout", action='store_true')
parser.add_argument("--verbose", help="Output verbose status messages", action='store_true')
parser.add_argument("--limit", help="Limit news topics if this parameter is provided", type=int)
args = parser.parse_args()

if __name__ == "__main__":
    parser = Parser()
    parser(url=args.source, stdout_json=args.json, stdout_verbose=args.verbose, limit=args.limit)
