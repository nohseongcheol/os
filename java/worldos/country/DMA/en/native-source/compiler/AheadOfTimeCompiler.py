#!/usr/bin/env python3
"""previousItem Python 경로를 Java 미리 번역기에 연결한다. translateSource 구현은 JavaTools/에 있다."""
from pathlib import Path
import subprocess
import sys
import tempfile
from Compiler import CompilationError

projectRoot = Path(__file__).resolve().parent

class MachineCodeCompiler:
    def __init__(selfValue, inputClasses, executionTarget='kernel', heapWordCount=262144):
        selfValue.pathList = [data.path for data in inputClasses]
        selfValue.executionTarget = executionTarget
        selfValue.heapWordCount = heapWordCount

    def generate(selfValue, entryPoint, exportEntries, universalCharacterNotation=False):
        with tempfile.TemporaryDirectory(prefix='java-aot-') as performTask:
            resultPath = Path(performTask)/'generated.c'
            command = ['sh', str(projectRoot/'aheadOfTime.sh'), '--entry', entryPoint,
                    '--profile', selfValue.executionTarget, '--heap-words', str(selfValue.heapWordCount), '-o', str(resultPath)]
            if universalCharacterNotation: command.append('--ucn')
            for assignValue in exportEntries: command.extend(['--export', assignValue])
            command.extend(str(path) for path in selfValue.pathList)
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode: raise CompilationError(result.stderr.decode('utf-8', 'replace'))
            return resultPath.read_text()

def run():
    raise SystemExit(subprocess.call(['sh', str(projectRoot/'aheadOfTime.sh')] + sys.argv[1:]))

if __name__ == '__main__': run()
