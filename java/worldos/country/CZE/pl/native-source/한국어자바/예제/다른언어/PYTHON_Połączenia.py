#!/usr/bin/env python3
"""dołączać_wpis Python 패키지 없이 polski Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def kod_znaku_ILE_LICZB(treść_WARTOŚĆ_cb0f2404, biblioteka, Klasa_Katalog):
    WYNIK = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(biblioteka), str(Klasa_Katalog)]), '문자명령', treść_WARTOŚĆ_cb0f2404],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(WYNIK.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    argumenty = 인수해석.parse_args()
    print('Python → polski.자바.문자.kod_znaku_ILE_LICZB:',
          kod_znaku_ILE_LICZB(argumenty.text, argumenty.jar, argumenty.classes))
