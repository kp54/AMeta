import argparse
import copy
import csv
import json
import os
import os.path

import taglib


def list_tree(path):
    # 返値は相対パス

    ret = list()
    que = os.listdir(path)

    while que:
        tmp = que.pop(0)
        tmq = os.path.join(path, tmp)

        if os.path.isdir(tmq):
            # 以下のコードと等価
            # for i in os.listdir(tmq):
            #     que.append(os.path.join(tmp, i))

            que.extend(map(
                lambda x: os.path.join(tmp, x),
                os.listdir(tmq)
            ))

        elif os.path.isfile(tmq):
            ret.append(tmp)

    return ret


def absolutize_tree(tree, base):
    import os.path
    return list(map(lambda x: os.path.join(base, x), tree))


def filter_tree_ext(tree, exts):
    return list(filter(lambda x: os.path.splitext(x)[1] in exts, tree))


def extract_tags(path):
    try:
        fp = taglib.File(path)
    except OSError:
        raise

    else:
        try:
            ret = copy.deepcopy(fp.tags)

        finally:
            fp.close()
    return ret


def dump_dict_json(dict_):
    return json.dumps(dict_, ensure_ascii=False)


def dump_list_csv(path, list_):
    with open(path, 'w', newline='') as fp:
        w = csv.writer(fp)
        for r in list_:
            w.writerow(r)

    return


def main():
    PATH = '/path/to/library/'
    EXTS = ['.flac', '.mp3']
    COLS = [
        'TITLE',
        'TITLESORT',
        'ARTIST',
        'ARTISTSORT',
        'COMPOSER',
        'DATE',
        'GENRE',
        'ALBUM',
        'ALBUMSORT',
        'ALBUMARTIST',
        'ALBUMARTISTSORT',
        'TRACKNUMBER',
        'TOTALTRACKS',
        'DISCNUMBER',
        'DISCTOTAL',
    ]
    HEADER = ['PATH'] + COLS + ['OTHERS']

    tree = list_tree(PATH)

    tree_abs = absolutize_tree(tree, PATH)

    tree_abs_audio = filter_tree_ext(tree_abs, EXTS)

    tree_abs_audio.sort()

    meta_dict_list = list(map(
        extract_tags,
        tree_abs_audio
    ))

    meta_serial_list = list(map(
        lambda x: [x.get(i, [''])[0] for i in COLS],
        meta_dict_list
    ))

    meta_dict_list_extra = list(map(
        lambda x: dict(filter(
            lambda y: y[0] not in COLS,
            x.items()
        )),
        meta_dict_list
    ))

    meta_json_list_extra = list(map(
        dump_dict_json,
        meta_dict_list_extra
    ))

    # 以下のコードと等価
    # sheet = [HEADER]
    # for i in range(len(tree_abs_audio)):
    #     sheet.append(
    #         [tree_abs_audio[i]]
    #         + meta_serial_list[i]
    #         + [meta_json_list_extra[i]]
    #     )
    sheet = [HEADER]+list(zip(
        tree_abs_audio, *zip(*meta_serial_list), meta_json_list_extra))

    dump_list_csv('tags.csv', sheet)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
