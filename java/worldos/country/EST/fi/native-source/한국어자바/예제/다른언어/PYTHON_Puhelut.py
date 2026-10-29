#!/usr/bin/env python3
"""liitä_merkintä Python 패키지 없이 suomi Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def koodipiste_LASKE(Sisältö_ARVO, kirjasto, Luokka_Directory):
    TULOS = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(kirjasto), str(Luokka_Directory)]), '문자명령', Sisältö_ARVO],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(TULOS.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    argumentit = 인수해석.parse_args()
    print('Python → suomi.자바.문자.koodipiste_LASKE:',
          koodipiste_LASKE(argumentit.text, argumentit.jar, argumentit.classes))
