#!/usr/bin/env python3
"""Připojit_položka Python 패키지 없이 čeština Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def bod_kódu_POČET(Obsah_HODNOTA, knihovna, Třída_Adresář):
    VÝSLEDEK = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(knihovna), str(Třída_Adresář)]), '문자명령', Obsah_HODNOTA],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(VÝSLEDEK.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    argumenty = 인수해석.parse_args()
    print('Python → čeština.자바.문자.bod_kódu_POČET:',
          bod_kódu_POČET(argumenty.text, argumenty.jar, argumenty.classes))
