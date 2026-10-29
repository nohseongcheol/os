#!/usr/bin/env python3
"""추가 Python 패키지 없이 한국어 Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def kôd_znaka_COUNT(Sadržaj_VALUE, biblioteka, klasa_Direktorij):
    mjera = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(biblioteka), str(klasa_Direktorij)]), '문자명령', Sadržaj_VALUE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(mjera.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Argumenti = 인수해석.parse_args()
    print('Python → 한국어.자바.문자.kôd_znaka_COUNT:',
          kôd_znaka_COUNT(Argumenti.text, Argumenti.jar, Argumenti.classes))
