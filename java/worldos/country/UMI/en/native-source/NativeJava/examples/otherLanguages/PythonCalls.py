#!/usr/bin/env python3
"""appendEntry Python 패키지 없이 English Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def codePointCount(contentValue, library, classDirectory):
    result = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(library), str(classDirectory)]), 'TextCommands', contentValue],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(result.stdout.strip())


if __name__ == '__main__':
    parseArguments = argparse.ArgumentParser(description=__doc__)
    parseArguments.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/NativeJava.jar'))
    parseArguments.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    parseArguments.add_argument('--text', default='한글 😀')
    arguments = parseArguments.parse_args()
    print('Python → English.Java.Characters.codePointCount:',
          codePointCount(arguments.text, arguments.jar, arguments.classes))
