#!/usr/bin/env python3
"""Annexa_introducció Python 패키지 없이 Català Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def codi_de_caràcter_COMPT(contingut_VALOR, biblioteca, Classe_directori):
    RESULTAT = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(biblioteca), str(Classe_directori)]), '문자명령', contingut_VALOR],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(RESULTAT.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    인수 = 인수해석.parse_args()
    print('Python → Català.자바.문자.codi_de_caràcter_COMPT:',
          codi_de_caràcter_COMPT(인수.text, 인수.jar, 인수.classes))
