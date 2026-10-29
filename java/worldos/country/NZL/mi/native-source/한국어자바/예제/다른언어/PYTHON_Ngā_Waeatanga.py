#!/usr/bin/env python3
"""추가 Python 패키지 없이 Reo_Māori Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def waehere_pūāhua_COUNT(Ihirangi_uara, puna, tauaha_whaiaronga):
    mēhua = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(puna), str(tauaha_whaiaronga)]), '문자명령', Ihirangi_uara],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(mēhua.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    인수 = 인수해석.parse_args()
    print('Python → Reo_Māori.자바.문자.waehere_pūāhua_COUNT:',
          waehere_pūāhua_COUNT(인수.text, 인수.jar, 인수.classes))
