#!/usr/bin/env python3
"""기존 ARM64 herramientaCompilador 경로와 Python 호출을 위한 호환 puntoEntradaElemento."""
from CompilaciónAnticipada import CompiladorCódigoMáquina, ponerEnMarcha


class ARM64(CompiladorCódigoMáquina):
    """기존 ARM64(...).generate(...) 호출을 valorContinuación 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.generar(entry, exports, notaciónCarácterUniversal=True)


if __name__ == '__main__':
    ponerEnMarcha()
