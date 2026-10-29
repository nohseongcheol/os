#!/usr/bin/env python3
"""기존 ARM64 compilatore_strumento 경로와 Python 호출을 위한 호환 punto_di_ingresso."""
from 기계어미리번역 import computer_CODICE_compilatore, avvia


class ARM64(computer_CODICE_compilatore):
    """기존 ARM64(...).generate(...) 호출을 이어 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.generare(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    avvia()
