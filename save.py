def load_list_csv(path):
    import csv

    with open(path, 'r', newline='') as fp:
        ret = list(csv.reader(fp))

    return ret


def overwrite_tags(path, tags):
    import taglib

    try:
        fp = taglib.File(path)
    except OSError:
        raise

    else:
        try:
            fp.tags = tags
            fp.save()

        finally:
            fp.close()
    return


def main():
    sheet = load_list_csv('tags.csv')
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
