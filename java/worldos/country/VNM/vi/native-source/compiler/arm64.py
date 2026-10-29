#!/usr/bin/env python3
"""기존 ARM64 côngCụTrìnhBiênDịch 경로와 Python 호출을 위한 호환 điểmMục."""
from BiênDịchTrước import TrìnhBiênDịchMãMáy, chạy


class ARM64(TrìnhBiênDịchMãMáy):
    """기존 ARM64(...).generate(...) 호출을 giáTrịSựTiếpDiễn 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.sinh(entry, exports, cáchKýHiệuKýTựPhổQuát=True)


if __name__ == '__main__':
    chạy()
