#!/usr/bin/env python3
"""français C 식별자만 UCN으로 옮긴다. Chaîne·Caractères·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

valeurJeton = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<valeurIdentificateur>[^\W\d]\w*)', re.S | re.M)

def convertirValeur(source):
    def remplacerValeur(estÉgal):
        if estÉgal.lastgroup == '보존':
            return estÉgal[0]
        return ''.join(valeurCaractère if ord(valeurCaractère) < 128 else
                       ('\\u%04x' if ord(valeurCaractère) <= 65535 else '\\U%08x') % ord(valeurCaractère)
                       for valeurCaractère in estÉgal[0])
    return valeurJeton.sub(remplacerValeur, source)

def exécuterCommande():
    Analyseur = argparse.ArgumentParser()
    Analyseur.add_argument('original', type=Path)
    Analyseur.add_argument('Sortie', type=Path)
    arguments = Analyseur.parse_args()
    for Fichier in sorted(arguments.original.rglob('*')):
        if Fichier.suffix not in ('.c', '.h'):
            continue
        Sortie = arguments.Sortie / Fichier.relative_to(arguments.original)
        Sortie.parent.mkdir(parents=True, exist_ok=True)
        sourceNouveau = convertirValeur(Fichier.read_text())
        if not Sortie.exists() or Sortie.read_text() != sourceNouveau:
            Sortie.write_text(sourceNouveau)

if __name__ == '__main__':
    exécuterCommande()
