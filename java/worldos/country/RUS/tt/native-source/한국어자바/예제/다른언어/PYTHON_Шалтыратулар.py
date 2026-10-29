#!/usr/bin/env python3
"""추가 Python 패키지 없이 Татарча Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def символ_коды_COUNT(Эчтәлек_VALUE, библиотека, класс_каталог):
    үлчәм = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(библиотека), str(класс_каталог)]), '문자명령', Эчтәлек_VALUE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(үлчәм.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    인수 = 인수해석.parse_args()
    print('Python → Татарча.자바.문자.символ_коды_COUNT:',
          символ_коды_COUNT(인수.text, 인수.jar, 인수.classes))
