import argparse
import csv

import taglib


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help='source file')

    return parser.parse_args()


def overwrite_tags(path, tags):
    fp = None
    try:
        fp = taglib.File(path)
        fp.tags = tags
        fp.save()
    finally:
        if fp:
            fp.close()
    return


def main():
    args = parse_args()
    config['source'] = args.src

    with open(config['source']) as fp:
        rd = csv.reader(fp)
        sheet = [list(r) for r in rd]

    # 1行目のヘッダを分離
    header, sheet = sheet[0][1:], sheet[1:]

    for r in sheet:
        path = r[0]

        # zipで (HEADER, CELL)
        tags = dict(zip(header, map(lambda x: [x], r[1:])))

        # 空要素を除去
        tags = dict(filter(
            lambda x: x[1][0] != '',
            tags.items()
        ))

        overwrite_tags(path, tags)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
