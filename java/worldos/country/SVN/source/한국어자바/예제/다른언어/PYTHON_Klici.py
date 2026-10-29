#!/usr/bin/env python3
"""dodati_vnos Python 패키지 없이 slovenščina Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def koda_znaka_COUNT(vsebina_VALUE, knjižnica, Razred_Imenik):
    REZULTAT = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(knjižnica), str(Razred_Imenik)]), '문자명령', vsebina_VALUE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(REZULTAT.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Argumenti = 인수해석.parse_args()
    print('Python → slovenščina.자바.문자.koda_znaka_COUNT:',
          koda_znaka_COUNT(Argumenti.text, Argumenti.jar, Argumenti.classes))
