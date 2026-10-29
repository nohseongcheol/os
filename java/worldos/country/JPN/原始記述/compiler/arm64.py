#!/usr/bin/env python3
"""기존 ARM64 コンパイラ道具要素 경로와 Python 호출을 위한 호환 入口点."""
from 事前用時間コンパイラ import 機械コードコンパイラ, 起動処理


class ARM64(機械コードコンパイラ):
    """기존 ARM64(...).generate(...) 호출을 継続状態値 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.生成(entry, exports, 汎用文字表記=True)


if __name__ == '__main__':
    起動処理()
