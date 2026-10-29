#!/usr/bin/env python3
"""기존 ARM64 компілятор_інструмент 경로와 Python 호출을 위한 호환 запис_бал."""
from 기계어미리번역 import комп_ютер_код_компілятор, запустити


class ARM64(комп_ютер_код_компілятор):
    """기존 ARM64(...).generate(...) 호출을 이어 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.генерувати(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    запустити()
