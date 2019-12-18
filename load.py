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


def main():
    with open('config.json') as fp:
        config = json.load(fp)

    header = ['PATH'] + config['columns'] + ['OTHERS']

    tree = list_tree(config['path'])

    tree_abs = absolutize_tree(tree, config['path'])

    tree_abs_audio = filter_tree_ext(tree_abs, config['extensions'])

    tree_abs_audio.sort()

    meta_dict_list = list(map(
        extract_tags,
        tree_abs_audio
    ))

    meta_serial_list = list(map(
        lambda x: [x.get(i, [''])[0] for i in config['columns']],
        meta_dict_list
    ))

    meta_dict_list_extra = list(map(
        lambda x: dict(filter(
            lambda y: y[0] not in config['columns'],
            x.items()
        )),
        meta_dict_list
    ))

    meta_json_list_extra = list(map(
        lambda x: json.dumps(x, ensure_ascii=False),
        meta_dict_list_extra
    ))

    sheet = [header]+list(zip(
        tree_abs_audio, *zip(*meta_serial_list), meta_json_list_extra))

    with open('tags.csv', 'w', newline='') as fp:
        w = csv.writer(fp)
        for r in sheet:
            w.writerow(r)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
