#!/usr/bin/env python3
"""Anexar_introdución Python 패키지 없이 Galego Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def código_de_carácter_CONTAR(Contido_VALOR, biblioteca, Clase_directorio):
    RESULTANTE = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(biblioteca), str(Clase_directorio)]), '문자명령', Contido_VALOR],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(RESULTANTE.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    Argumentos = 인수해석.parse_args()
    print('Python → Galego.자바.문자.código_de_carácter_CONTAR:',
          código_de_carácter_CONTAR(Argumentos.text, Argumentos.jar, Argumentos.classes))
