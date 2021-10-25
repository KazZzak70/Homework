from date_converter import check_user_date
from parser_engine import Parser
import args as _args
import logging

if __name__ == "__main__":
    args = _args.configure_parser()
    if args.date is not None:
        check_user_date(args.date)
    if args.limit is not None and args.limit < 0:
        logging.error(msg="Wrong value of limit param")
        exit()
    parser = Parser()
    parser(url=args.source, stdout_json=args.json, stdout_verbose=args.verbose, limit=args.limit, date=args.date,
           pdf=args.to_pdf, fb2=args.to_fb2)
