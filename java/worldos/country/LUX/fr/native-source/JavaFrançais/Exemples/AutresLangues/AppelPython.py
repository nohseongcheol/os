#!/usr/bin/env python3
"""ajouterFinEntréeÉlément Python 패키지 없이 français Java 메서드의 결과를 받는다."""
import argparse
import os
from pathlib import Path
import subprocess


def nombreÉlémentsPointCode(valeurContenuValeur, bibliothèque, répertoireClasse):
    résultat = subprocess.run(
        ['java', '-Dfile.encoding=UTF-8', '-cp',
         os.pathsep.join([str(bibliothèque), str(répertoireClasse)]), 'CommandeTexte', valeurContenuValeur],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        encoding='utf-8', timeout=60)
    return int(résultat.stdout.strip())


if __name__ == '__main__':
    analyserArguments = argparse.ArgumentParser(description=__doc__)
    analyserArguments.add_argument('--jar', type=Path, default=Path('/opt/jkoros/lib/JavaFrançais.jar'))
    analyserArguments.add_argument('--classes', type=Path, default=Path(__file__).resolve().parent / 'classes')
    analyserArguments.add_argument('--text', default='한글 😀')
    arguments = analyserArguments.parse_args()
    print('Python → français.Java.Caractères.nombreÉlémentsPointCode:',
          nombreÉlémentsPointCode(arguments.text, arguments.jar, arguments.classes))
