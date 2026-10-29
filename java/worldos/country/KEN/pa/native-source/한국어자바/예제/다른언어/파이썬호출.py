#!/usr/bin/env python3
"""추가 Python 패키지 없이 ਪੰਜਾਬੀ Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def 코드포인트수(ਤਤਕਰਾ_ਕੀਮਤ, ਪੁਸਤਕਾਲਾ, ਸ੍ਰੇਣੀ_ਨਿਰਦੇਸ਼ਕ):
    ਮਾਪ = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(ਪੁਸਤਕਾਲਾ), str(ਸ੍ਰੇਣੀ_ਨਿਰਦੇਸ਼ਕ)]), '문자명령', ਤਤਕਰਾ_ਕੀਮਤ],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(ਮਾਪ.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    ਆਰਗੂਮੈਂਟ = 인수해석.parse_args()
    print('Python → ਪੰਜਾਬੀ.자바.문자.코드포인트수:',
          코드포인트수(ਆਰਗੂਮੈਂਟ.text, ਆਰਗੂਮੈਂਟ.jar, ਆਰਗੂਮੈਂਟ.classes))
