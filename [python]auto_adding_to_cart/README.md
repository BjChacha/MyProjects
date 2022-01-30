# Automatically Adding Item to Cart in JD.com

> Used for books purchase in some cases.

## Required

- Python 3+

## Features

- As the title said, automatically, adding, cart.
- Save your junk time to do more junk things.
- Bugs to fixed.

## Usage

1. Clone or download this project;
2. Rename your book list file to `books.csv` and the format should be like:
    | BUYER_NAME | BOOK_NAME | BOOK_URL                               | BOOK_NUM |
    |------------|-----------|----------------------------------------|----------|
    | Tommy      | 非暴力沟通     | https://item.jd.com/12419935.html | 1        |
    | ...        |           |                                        |          |
3. Fill your browser cookie of [jd.com](https://www.jd.com/) in `config.json`;
4. Run `python main.py` in your terminal.

## Notice

- Feel free to remove the `remain_books.tmp` file if anything goes wrong.

## BUG

- The number of successes does not match the actual.
- I know more, but you tell me.


## TODO

- [ ] Identify whether an item is in stock or not.