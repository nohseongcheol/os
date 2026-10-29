#!/usr/bin/env python3
"""Deutsch C 식별자만 UCN으로 옮긴다. Zeichenkette·Zeichen·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

wortzeichenWert = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<bezeichnerWert>[^\W\d]\w*)', re.S | re.M)

def wertUmwandeln(Quelltext):
    def wertErsetzen(istGleich):
        if istGleich.lastgroup == '보존':
            return istGleich[0]
        return ''.join(zeichenWert if ord(zeichenWert) < 128 else
                       ('\\u%04x' if ord(zeichenWert) <= 65535 else '\\U%08x') % ord(zeichenWert)
                       for zeichenWert in istGleich[0])
    return wortzeichenWert.sub(wertErsetzen, Quelltext)

def befehlAusführen():
    Strukturanalysierer = argparse.ArgumentParser()
    Strukturanalysierer.add_argument('ursprünglich', type=Path)
    Strukturanalysierer.add_argument('Ausgabe', type=Path)
    argumente = Strukturanalysierer.parse_args()
    for Datei in sorted(argumente.ursprünglich.rglob('*')):
        if Datei.suffix not in ('.c', '.h'):
            continue
        Ausgabe = argumente.Ausgabe / Datei.relative_to(argumente.ursprünglich)
        Ausgabe.parent.mkdir(parents=True, exist_ok=True)
        neuQuelltext = wertUmwandeln(Datei.read_text())
        if not Ausgabe.exists() or Ausgabe.read_text() != neuQuelltext:
            Ausgabe.write_text(neuQuelltext)

if __name__ == '__main__':
    befehlAusführen()
