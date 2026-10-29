#!/usr/bin/env python3
"""προσαρτώ_καταχώρηση Python 패키지 없이 ελληνικά Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def 코드포인트수(Περιεχόμενο_τιμή, βιβλιοθήκη, Τάξη_Κατάλογος):
    μέτρηση = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(βιβλιοθήκη), str(Τάξη_Κατάλογος)]), '문자명령', Περιεχόμενο_τιμή],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(μέτρηση.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Παράμετροι = 인수해석.parse_args()
    print('Python → ελληνικά.자바.문자.코드포인트수:',
          코드포인트수(Παράμετροι.text, Παράμετροι.jar, Παράμετροι.classes))
