#!/usr/bin/env python3
"""Lägga_till_post Python 패키지 없이 Svenska Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def kodpunkt_ANTAL(Innehåll_värde, bibliotek, Kurs_Katalog):
    RESULTAT = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(bibliotek), str(Kurs_Katalog)]), '문자명령', Innehåll_värde],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(RESULTAT.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    argument = 인수해석.parse_args()
    print('Python → Svenska.자바.문자.kodpunkt_ANTAL:',
          kodpunkt_ANTAL(argument.text, argument.jar, argument.classes))
