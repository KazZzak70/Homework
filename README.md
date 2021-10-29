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
* All received news are saved in `.json` format files in `/output_data/` folder in your home directory
* All `.pdf` and `.fb2` files are saved in a `/output_files/` folder in your home directory

The utility can be wrapped into distribution package with `setuptools`.
This package can export CLI utility named `rss_reader`.

## Installation

1. Clone the repo
   ```sh
   $ git clone https://github.com/KazZzak70/Homework.git
   ```
2. Go to the `Homework` folder
   ```sh
   $ cd Homework/
   ```
3. Switch to branch with the followed command:
   ```sh
   $ git checkout -b final_task origin/final_task
   ```
4. Install required external dependencies from file `requirements.txt` with the followed command:
   ```sh
   $ pip install -r requirements.txt
   ```
5. To install a package to run it from anywhere, use the followed command:
   ```sh
   $ pip install -e .
   ```

## Usage

Utility can be used in a few ways. 

First:

* Go to the `/Homework/rss_reader/` folder.

* Run below command (optional arguments write on your own):
   ```sh
   $ python rss_reader.py {source URL here} --limit 1 --date 20211030 --json --verbose --to-fb2 --to-pdf
   ```
Second (CLI utility):

* After completion of the fifth paragraph of **Installation** you can use utility this way:

   ```sh
   $ rss_reader {source URL here} --limit 1 -- date 20211030 --json --verbose --to-fb2 --to-pdf
   ```
###There are three main modes of use:
1. User defines `source` argument with the link to the RSS channel and do not define `--date` argument
   _*In this mode Internet connection required.*_ All data will be saved to local `.json` format file.
   ```sh
   $ python rss_reader.py {source URL here} --limit 1 --json --verbose --to-pdf --to-fb2
   ```
   or after the completion of the fifth paragraph of **Installation**:
   ```sh
   $ rss_reader {source URL here} --limit 1 --json --verbose --to-pdf --to-fb2
   ```
2. User defines `source` argument with the link to the RSS channel with `--date` argument to sort news by their pubdate
   This mode does not require Internet connection. Data will be read from the locally saved `.json` format file.
   If no matching data file will be found, an appropriate ***error*** will be returned.
   ```sh
   $ rss_reader {source URL here} --date 20211030 --limit 1 --json --verbose --to-pdf --to-fb2
   ```
3. User does not define `source` argument, but define `--date` argument to sort all locally saved news by their pubdate
   This mode does not require Internet connection. Data will be read from all locally saved `.json` format files.
   ```sh
   $ rss_reader --date 20211030 --limit 1 --json --verbose --to-pdf --to-fb2
   ```
## JSON-file structure:
```
{
    "feed": resource name,
    "items": [
        {
            "title": news title,
            "description": news description,
            "link": link to news,
            "pubdate": news publication date,
            "links": {
                "1": link to news,
                "2": link to some media
            }
        },
        ...
        ]
}
```
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
