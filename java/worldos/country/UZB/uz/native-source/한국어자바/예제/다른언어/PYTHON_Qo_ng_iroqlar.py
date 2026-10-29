#!/usr/bin/env python3
"""추가 Python 패키지 없이 한국어 Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def belgi_kodi_COUNT(tarkib_VALUE, kutubxona, Sinf_katalog):
    o_lchov = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(kutubxona), str(Sinf_katalog)]), '문자명령', tarkib_VALUE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(o_lchov.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    인수 = 인수해석.parse_args()
    print('Python → 한국어.자바.문자.belgi_kodi_COUNT:',
          belgi_kodi_COUNT(인수.text, 인수.jar, 인수.classes))
