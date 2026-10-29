#!/usr/bin/env python3
"""기존 ARM64 คอมไพเลอร์_เครื่องมือ 경로와 Python 호출을 위한 호환 จุดเข้าใช้งาน."""
from 기계어미리번역 import เครื่อง_รหัส_คอมไพเลอร์, เรียกใช้งาน


class ARM64(เครื่อง_รหัส_คอมไพเลอร์):
    """기존 ARM64(...).generate(...) 호출을 이어 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.สร้าง_167eff27(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    เรียกใช้งาน()
