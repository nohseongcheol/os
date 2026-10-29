#!/usr/bin/env python3
"""기존 ARM64 компилятор_средство 경로와 Python 호출을 위한 호환 точка_входа."""
from ПредварительныйКомпилятор import компьютер_код_компилятор, запустить


class ARM64(компьютер_код_компилятор):
    """기존 ARM64(...).generate(...) 호출을 이어 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.генерировать(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    запустить()
