#!/usr/bin/env python3
"""기존 ARM64 компилатор_инструмент 경로와 Python 호출을 위한 호환 запис_пункт."""
from 기계어미리번역 import машина_код_компилатор, Стартиране


class ARM64(машина_код_компилатор):
    """기존 ARM64(...).generate(...) 호출을 이어 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.генерирам(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    Стартиране()
