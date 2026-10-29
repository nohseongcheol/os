#!/usr/bin/env python3
"""hozzáfűz_bejegyzés Python 패키지 없이 magyar Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def kódpont_DARAB(Tartalom_ÉRTÉK, kódtár, tanóra_címtár):
    KR = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(kódtár), str(tanóra_címtár)]), '문자명령', Tartalom_ÉRTÉK],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(KR.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Argumentumok = 인수해석.parse_args()
    print('Python → magyar.자바.문자.kódpont_DARAB:',
          kódpont_DARAB(Argumentumok.text, Argumentumok.jar, Argumentumok.classes))
