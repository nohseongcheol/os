#!/usr/bin/env python3
"""sujungti_įrašas Python 패키지 없이 Lietuvių Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def kodo_elementas_COUNT(Turinys_VALUE, biblioteka, klasė_Katalogas):
    REZULTATAS = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(biblioteka), str(klasė_Katalogas)]), '문자명령', Turinys_VALUE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(REZULTATAS.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Argumentai = 인수해석.parse_args()
    print('Python → Lietuvių.자바.문자.kodo_elementas_COUNT:',
          kodo_elementas_COUNT(Argumentai.text, Argumentai.jar, Argumentai.classes))
