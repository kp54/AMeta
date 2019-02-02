# ファイルのタグを吐くツール

import os.path
import sys

import taglib


def main():
    if len(sys.argv) < 1:
        return -1
    if not(os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1])):
        return -2

    try:
        f = taglib.File(sys.argv[1])
    except OSError:
        return -3
    else:
        try:
            for k, v in f.tags.items():
                print(f'{k}: {v}')
        finally:
            f.close()


if __name__ == '__main__':
    sys.exit(main())
