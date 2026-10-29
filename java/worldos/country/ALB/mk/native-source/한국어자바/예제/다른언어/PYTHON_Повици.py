#!/usr/bin/env python3
"""추가 Python 패키지 없이 Македонски Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def кодна_точка_COUNT(Содржина_VALUE, библиотека, класа_Именик):
    мерка = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(библиотека), str(класа_Именик)]), '문자명령', Содржина_VALUE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(мерка.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Аргументи = 인수해석.parse_args()
    print('Python → Македонски.자바.문자.кодна_точка_COUNT:',
          кодна_точка_COUNT(Аргументи.text, Аргументи.jar, Аргументи.classes))
