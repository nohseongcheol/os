#!/usr/bin/env python3
"""adăuga_intrare Python 패키지 없이 Română Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def cod_caracter_COUNT(Conținut_VALUE, bibliotecă, Clasă_Director):
    KR = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(bibliotecă), str(Clasă_Director)]), '문자명령', Conținut_VALUE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(KR.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Argumente = 인수해석.parse_args()
    print('Python → Română.자바.문자.cod_caracter_COUNT:',
          cod_caracter_COUNT(Argumente.text, Argumente.jar, Argumente.classes))
