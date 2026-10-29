#!/usr/bin/env python3
"""기존 ARM64 編譯器工具 경로와 Python 호출을 위한 호환 條目分."""
from 提前所屬時間編譯器 import 計算機程式碼編譯器, 運行


class ARM64(計算機程式碼編譯器):
    """기존 ARM64(...).generate(...) 호출을 繼續狀態值 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.生成(entry, exports, 通用字元表示法=True)


if __name__ == '__main__':
    運行()
