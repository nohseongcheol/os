#!/usr/bin/env python3
"""Tilføye_oppføring Python 패키지 없이 norsk Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def tegnkode_ANTALL(Innhold_VERDI, bibliotek, time_katalog):
    KR = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(bibliotek), str(time_katalog)]), '문자명령', Innhold_VERDI],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(KR.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Argumenter = 인수해석.parse_args()
    print('Python → norsk.자바.문자.tegnkode_ANTALL:',
          tegnkode_ANTALL(Argumenter.text, Argumenter.jar, Argumenter.classes))
