#!/usr/bin/env python3
"""기존 ARM64 compilador_ferramenta 경로와 Python 호출을 위한 호환 ponto_de_entrada."""
from CompiladorAntecipado import computador_CÓDIGO_compilador, iniciar


class ARM64(computador_CÓDIGO_compilador):
    """기존 ARM64(...).generate(...) 호출을 이어 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.gerar(entry, exports, 범용문자표기=True)


if __name__ == '__main__':
    iniciar()
