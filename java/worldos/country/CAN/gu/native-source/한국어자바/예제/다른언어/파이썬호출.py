#!/usr/bin/env python3
"""추가 Python 패키지 없이 ગુજરાતી Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def 코드포인트수(સામગ્રી_મૂલ્ય, લાઇબ્રેરી, વર્ગ_નિર્દેશિકા):
    પરિમાણ = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(લાઇબ્રેરી), str(વર્ગ_નિર્દેશિકા)]), '문자명령', સામગ્રી_મૂલ્ય],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(પરિમાણ.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    દલીલો = 인수해석.parse_args()
    print('Python → ગુજરાતી.자바.문자.코드포인트수:',
          코드포인트수(દલીલો.text, દલીલો.jar, દલીલો.classes))
