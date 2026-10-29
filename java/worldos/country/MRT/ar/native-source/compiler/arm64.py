#!/usr/bin/env python3
"""기존 ARM64 محول_برمجي_أداة 경로와 Python 호출을 위한 호환 نقطة_الإدخال."""
from مترجممسبق import جهاز_رمز_محول_برمجي, تشغيل


class ARM64(جهاز_رمز_محول_برمجي):
    """기존 ARM64(...).generate(...) 호출을 이어 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.إنشاء(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    تشغيل()
