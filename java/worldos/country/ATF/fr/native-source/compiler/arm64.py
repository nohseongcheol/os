#!/usr/bin/env python3
"""기존 ARM64 outilCompilateur 경로와 Python 호출을 위한 호환 pointEntréeÉlément."""
from CompilationAnticipée import CompilateurCodeMachine, lancer


class ARM64(CompilateurCodeMachine):
    """기존 ARM64(...).generate(...) 호출을 valeurContinuation 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.générer(entry, exports, notationCaractèreUniversel=True)


if __name__ == '__main__':
    lancer()
