#!/usr/bin/env python3
"""Lisa_kirje Python 패키지 없이 Eesti Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def koodipunkt_COUNT(Sisu_VALUE, teek, tund_kaust):
    TULEMUS = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(teek), str(tund_kaust)]), '문자명령', Sisu_VALUE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(TULEMUS.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Argumendid = 인수해석.parse_args()
    print('Python → Eesti.자바.문자.koodipunkt_COUNT:',
          koodipunkt_COUNT(Argumendid.text, Argumendid.jar, Argumendid.classes))
