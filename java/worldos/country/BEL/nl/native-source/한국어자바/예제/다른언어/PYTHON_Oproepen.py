#!/usr/bin/env python3
"""toevoegen_invoer Python 패키지 없이 Nederlands Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def codepoint_AANTAL(Inhoud_WAARDE, bibliotheek, les_map):
    resultaat = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(bibliotheek), str(les_map)]), '문자명령', Inhoud_WAARDE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(resultaat.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    argumenten = 인수해석.parse_args()
    print('Python → Nederlands.자바.문자.codepoint_AANTAL:',
          codepoint_AANTAL(argumenten.text, argumenten.jar, argumenten.classes))
