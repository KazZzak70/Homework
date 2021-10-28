from rss_reader.date_converter import check_user_date
from rss_reader.parser_engine import Parser
from rss_reader import args as _args
import logging


def rss_reader():
    args = _args.configure_parser().parse_args()
    if args.date is not None:
        check_user_date(args.date)
    if args.limit is not None and args.limit < 0:
        logging.error(msg="Wrong value of limit param")
        exit()
    parser = Parser()
    parser(url=args.source, stdout_json=args.json, stdout_verbose=args.verbose, limit=args.limit, date=args.date,
           pdf=args.to_pdf, fb2=args.to_fb2)


if __name__ == '__main__':
    rss_reader()
