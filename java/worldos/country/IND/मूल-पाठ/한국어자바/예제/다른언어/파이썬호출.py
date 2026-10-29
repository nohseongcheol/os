#!/usr/bin/env python3
"""जोड़ें_एन्ट्री Python 패키지 없이 हिंदी Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def 코드포인트수(सामग्री_मान, लाइब्रेरी, कक्षा_डायरेक्टरी):
    परिणाम = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(लाइब्रेरी), str(कक्षा_डायरेक्टरी)]), '문자명령', सामग्री_मान],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(परिणाम.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    तर्क = 인수해석.parse_args()
    print('Python → हिंदी.자바.문자.코드포인트수:',
          코드포인트수(तर्क.text, तर्क.jar, तर्क.classes))
