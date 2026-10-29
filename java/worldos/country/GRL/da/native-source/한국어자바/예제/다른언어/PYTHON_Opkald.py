#!/usr/bin/env python3
"""tilføj_post Python 패키지 없이 Dansk Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def tegnkode_TÆL(Indhold_VÆRDI, bibliotek, Hold_mappe):
    KR = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(bibliotek), str(Hold_mappe)]), '문자명령', Indhold_VÆRDI],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(KR.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Argumenter = 인수해석.parse_args()
    print('Python → Dansk.자바.문자.tegnkode_TÆL:',
          tegnkode_TÆL(Argumenter.text, Argumenter.jar, Argumenter.classes))
