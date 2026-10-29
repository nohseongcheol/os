#!/usr/bin/env python3
"""기존 ARM64 übersetzerWerkzeug 경로와 Python 호출을 위한 호환 eintragPunkt."""
from Vorabübersetzung import MaschineKodeÜbersetzer, ausführenVorgang


class ARM64(MaschineKodeÜbersetzer):
    """기존 ARM64(...).generate(...) 호출을 fortsetzungWert 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.generieren(entry, exports, allgemeingültigZeichenSchreibweise=True)


if __name__ == '__main__':
    ausführenVorgang()
