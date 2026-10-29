#!/usr/bin/env python3
"""추가 Python 패키지 없이 ಕನ್ನಡ Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def 코드포인트수(ವಿಷಯ_ಮೌಲ್ಯ, ಲೈಬ್ರರಿ, ವರ್ಗ_ಡೈರೆಕ್ಟರಿ):
    ಮಾಪನ = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(ಲೈಬ್ರರಿ), str(ವರ್ಗ_ಡೈರೆಕ್ಟರಿ)]), '문자명령', ವಿಷಯ_ಮೌಲ್ಯ],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(ಮಾಪನ.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    인수 = 인수해석.parse_args()
    print('Python → ಕನ್ನಡ.자바.문자.코드포인트수:',
          코드포인트수(인수.text, 인수.jar, 인수.classes))
