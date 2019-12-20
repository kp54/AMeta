import argparse
import copy
import csv
import json
import os
import os.path

import taglib


def parse_args():
    default_columns = [
        "TITLE",
        "ARTIST",
        "COMPOSER",
        "DATE",
        "GENRE",
        "ALBUM",
        "ALBUMARTIST",
        "TRACKNUMBER",
        "TRACKTOTAL",
        "DISCNUMBER",
        "DISCTOTAL",
    ]

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--out', help='output filename', default='tags.csv')
    parser.add_argument('-c', '--config', help='config file', default=None)
    parser.add_argument('--exts', help='file extesion(s)', default='.flac,.mp3')
    parser.add_argument('--cols', help='tag name(s)', default=default_columns)
    parser.add_argument('src', help='source directory')

    return parser.parse_args()


def extract_tags(path):
    fp = None
    try:
        fp = taglib.File(path)
        ret = copy.deepcopy(fp.tags)
    finally:
        if fp:
            fp.close()
    return ret


def main():
    args = parse_args()
    if args.config:
        with open(args.config) as fp:
            config = json.load(fp)
    else:
        config = {
            'extensions': args.exts.split(','),
            'columns': args.cols,
        }
    config['path'] = args.src
    header = ['PATH'] + config['columns']

    extra = False
    sheet = [header]
    que = list(map(
        lambda x: os.path.join(config['path'], x),
        os.listdir(config['path'])
    ))
    while que:
        tmp = que.pop(0)

        if os.path.isdir(tmp):
            que.extend(map(
                lambda x: os.path.join(tmp, x),
                os.listdir(tmp)
            ))

        elif os.path.isfile(tmp):
            if os.path.splitext(tmp)[1] not in config['extensions']:
                continue
            tags = extract_tags(tmp)
            cols = [tmp]
            for c in config['columns']:
                if c in tags:
                    cols.append(tags[c][0])
                    del tags[c]
                else:
                    cols.append('')
            if tags:
                extra = True
                cols.append(json.dumps(tags, ensure_ascii=False))
            sheet.append(cols)

    if extra:
        header += ['OTHERS']
        for r in sheet:
            if len(header) != len(r):
                r.append("{}")

    with open('tags.csv', 'w', newline='') as fp:
        w = csv.writer(fp)
        for r in sheet:
            w.writerow(r)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
