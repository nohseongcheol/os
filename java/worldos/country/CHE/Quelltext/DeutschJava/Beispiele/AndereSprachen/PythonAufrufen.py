#!/usr/bin/env python3
"""eintragAnhängen Python 패키지 없이 Deutsch Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def kodePunktAnzahl(inhaltswertWert, bibliothek, klasseVerzeichnis):
    ergebnis = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(bibliothek), str(klasseVerzeichnis)]), 'Zeichenbefehl', inhaltswertWert],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(ergebnis.stdout.strip())


if __name__ == '__main__':
    argumenteAnalysieren = argparse.ArgumentParser(description=__doc__)
    argumenteAnalysieren.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/DeutschJava.jar'))
    argumenteAnalysieren.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    argumenteAnalysieren.add_argument('--text', default='한글 😀')
    argumente = argumenteAnalysieren.parse_args()
    print('Python → Deutsch.Java.Zeichen.kodePunktAnzahl:',
          kodePunktAnzahl(argumente.text, argumente.jar, argumente.classes))
