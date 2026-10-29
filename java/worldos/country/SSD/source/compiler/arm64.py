#!/usr/bin/env python3
"""기존 ARM64 compilerTool 경로와 Python 호출을 위한 호환 entryPoint."""
from AheadOfTimeCompiler import MachineCodeCompiler, run


class ARM64(MachineCodeCompiler):
    """기존 ARM64(...).generate(...) 호출을 continuationValue 준다."""
    def __init__(self, classes, profile='kernel', heap_words=262144):
        super().__init__(classes, profile, heap_words)

    def generate(self, entry, exports):
        return self.generate(entry, exports, universalCharacterNotation=True)


if __name__ == '__main__':
    run()
