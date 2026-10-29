#!/usr/bin/env python3
"""기존 ARM64 번역기 경로와 Python 호출을 위한 호환 প্রবিষ্ট_পইণ্ট."""
from 기계어미리번역 import 기계어번역기, সঞ্চালন


class ARM64(기계어번역기):
    """기존 ARM64(...).generate(...) 호출을 이어 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.সৃষ্টি_কৰক(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    সঞ্চালন()
