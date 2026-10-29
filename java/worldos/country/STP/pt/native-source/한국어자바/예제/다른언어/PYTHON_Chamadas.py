#!/usr/bin/env python3
"""Acrescentar_entrada Python 패키지 없이 Português Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def ponto_de_código_CONT_NÚM(Conteúdo_VALOR, biblioteca, aula_Diretório):
    resultado = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(biblioteca), str(aula_Diretório)]), '문자명령', Conteúdo_VALOR],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(resultado.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    argumentos = 인수해석.parse_args()
    print('Python → Português.자바.문자.ponto_de_código_CONT_NÚM:',
          ponto_de_código_CONT_NÚM(argumentos.text, argumentos.jar, argumentos.classes))
