#!/usr/bin/env python3
"""추가 Python 패키지 없이 বাংলা Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def 코드포인트수(সামগ্রি_মান, লাইব্রেরি, শ্রেণী_ডিরেক্টরি):
    পরিমাপ = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(লাইব্রেরি), str(শ্রেণী_ডিরেক্টরি)]), '문자명령', সামগ্রি_মান],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(পরিমাপ.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    আর্গুমেন্ট_তালিকা = 인수해석.parse_args()
    print('Python → বাংলা.자바.문자.코드포인트수:',
          코드포인트수(আর্গুমেন্ট_তালিকা.text, আর্গুমেন্ট_তালিকা.jar, আর্গুমেন্ট_তালিকা.classes))
