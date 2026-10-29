#!/usr/bin/env python3
"""추가 Python 패키지 없이 한국어 Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def 코드포인트수(មាតិកា_តំលៃ, បណ្ណាល័យ, ថ្នាក់_បញ្ជី):
    ការវាស់វែង = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(បណ្ណាល័យ), str(ថ្នាក់_បញ្ជី)]), '문자명령', មាតិកា_តំលៃ],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(ការវាស់វែង.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    អាគុយម៉ង់ = 인수해석.parse_args()
    print('Python → 한국어.자바.문자.코드포인트수:',
          코드포인트수(អាគុយម៉ង់.text, អាគុយម៉ង់.jar, អាគុយម៉ង់.classes))
