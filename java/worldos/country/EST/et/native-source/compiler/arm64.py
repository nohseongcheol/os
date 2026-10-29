#!/usr/bin/env python3
"""기존 ARM64 kompilaator_tööriist 경로와 Python 호출을 위한 호환 kirje_p."""
from 기계어미리번역 import arvuti_CODE_kompilaator, Käivita_2


class ARM64(arvuti_CODE_kompilaator):
    """기존 ARM64(...).generate(...) 호출을 이어 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.genereerima(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    Käivita_2()
