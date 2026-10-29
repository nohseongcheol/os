#!/usr/bin/env python3
"""Aggiunta_voce Python 패키지 없이 Italiano Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def punto_di_codice_CONTA_NUMERI(Contenuto_VALORE, Catalogo, Corso_elenco):
    risultato = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(Catalogo), str(Corso_elenco)]), '문자명령', Contenuto_VALORE],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(risultato.stdout.strip())


if __name__ == '__main__':
    인수해석 = argparse.ArgumentParser(description=__doc__)
    인수해석.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/한국어자바.jar'))
    인수해석.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    인수해석.add_argument('--text', default='한글 😀')
    argomenti = 인수해석.parse_args()
    print('Python → Italiano.자바.문자.punto_di_codice_CONTA_NUMERI:',
          punto_di_codice_CONTA_NUMERI(argomenti.text, argomenti.jar, argomenti.classes))
