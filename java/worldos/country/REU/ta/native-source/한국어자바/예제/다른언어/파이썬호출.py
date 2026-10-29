#!/usr/bin/env python3
"""추가 Python 패키지 없이 தமிழ் Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def 코드포인트수(உள்ளடக்கம்_மதிப்பு, நூலகம், பிரிவு_கோப்பகம்):
    அளவிடக்கூடியது = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(நூலகம்), str(பிரிவு_கோப்பகம்)]), '문자명령', உள்ளடக்கம்_மதிப்பு],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(அளவிடக்கூடியது.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    செயலுருபுகள் = 인수해석.parse_args()
    print('Python → தமிழ்.자바.문자.코드포인트수:',
          코드포인트수(செயலுருபுகள்.text, செயலுருபுகள்.jar, செயலுருபுகள்.classes))
