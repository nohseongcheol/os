#!/usr/bin/env python3
"""Pievienot_ievade Python 패키지 없이 Latviešu Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def koda_punkts_COUNT(Saturs_VALUE, bibliotēka, klase_Direktorijs):
    mērs = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(bibliotēka), str(klase_Direktorijs)]), '문자명령', Saturs_VALUE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(mērs.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Parametri = 인수해석.parse_args()
    print('Python → Latviešu.자바.문자.koda_punkts_COUNT:',
          koda_punkts_COUNT(Parametri.text, Parametri.jar, Parametri.classes))
