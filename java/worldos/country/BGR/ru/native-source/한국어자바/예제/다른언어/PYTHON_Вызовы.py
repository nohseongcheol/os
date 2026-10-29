#!/usr/bin/env python3
"""добавить_ввод Python 패키지 없이 русский Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def код_знака_СЧЁТ(контент_ЗНАЧЕН, библиотека, Класс_Каталог):
    результат = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(библиотека), str(Класс_Каталог)]), '문자명령', контент_ЗНАЧЕН],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(результат.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    аргументы = 인수해석.parse_args()
    print('Python → русский.자바.문자.код_знака_СЧЁТ:',
          код_знака_СЧЁТ(аргументы.text, аргументы.jar, аргументы.classes))
