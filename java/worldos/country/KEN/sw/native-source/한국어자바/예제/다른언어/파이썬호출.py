#!/usr/bin/env python3
"""추가 Python 패키지 없이 한국어 Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def 코드포인트수(maudhui_thamani, maktaba, tabaka_Saraka):
    결과 = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(maktaba), str(tabaka_Saraka)]), '문자명령', maudhui_thamani],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(결과.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    인수 = 인수해석.parse_args()
    print('Python → 한국어.자바.문자.코드포인트수:',
          코드포인트수(인수.text, 인수.jar, 인수.classes))
