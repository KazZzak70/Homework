## Pure Python command-line RSS reader.


RSS reader is a one-shot command-line utility which prints news in a human-readable format from specified `source `
and stores them to the specified files.
It uses the `argparse` module.

_**Python 3.9 is required.**_

The utility provides the following interface:

```
usage: rss_reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-pdf] [--to-fb2] [source]

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Output verbose status messages
  --limit LIMIT  Limit news topics if this parameter is provided
  --date DATE    Sort news for a given date
  --to-pdf       Export result to .pdf file format
  --to-fb2       Export result to .fb2 file format
```

## General requirements:
* Source URL provided in the `source` argument must contain `http` or `https` and `://` symbols.
* Optional `--date` argument must be provided in the `%Y%M%D` format, day and month from **01** to **09** in the `--date`
argument should start with **0**

This argument turn on offline mode, in which utility reads news from locally saved `.json` data files, so
use utility with specified `source` and no `--date` argument at least one time to make `/output_data/` folder contain 
some data to start using the `--date` argument mode.

* If `--date` and `--limit` arguments are not provided, all available news from a rss-page will be printed.
* if the user has set the `--limit` more than the number of news then the program prints all available news.
* The `--limit` and `--date` arguments also have influence on the `--to-pdf`, `--to-fb2` generation.
* If the `--version` option is specified, utility prints its version and exit.
* With the argument `--verbose` utility prints all logs at runtime in stdout.
* All received news are saved in `.json` format files in `/output_data/` folder
* All `.pdf` and `.fb2` files are saved in a `/output_files/` folder

The utility can be wrapped into distribution package with `setuptools`.
This package can export CLI utility named `rss_reader`.

## Installation

1. Clone the repo
   ```sh
   $ git clone https://github.com/KazZzak70/Homework.git
   ```
2. 