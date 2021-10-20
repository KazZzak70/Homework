from parser_engine import Parser
import args as _args


if __name__ == "__main__":
    args = _args.configure_parser()
    parser = Parser()
    parser(url=args.source, stdout_json=args.json, stdout_verbose=args.verbose, limit=args.limit)
