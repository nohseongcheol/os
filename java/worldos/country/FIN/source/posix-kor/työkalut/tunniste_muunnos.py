#!/usr/bin/env python3
"""suomi C 식별자만 UCN으로 옮긴다. merkkijono_ARVO·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

tunnus_ARVO_eb540501 = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<tunniste_ARVO>[^\W\d]\w*)', re.S | re.M)

def MUUNNA_ARVO(lähdetiedosto):
    def KORVAA_ARVO(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(merkki_ARVO if ord(merkki_ARVO) < 128 else
                       ('\\u%04x' if ord(merkki_ARVO) <= 65535 else '\\U%08x') % ord(merkki_ARVO)
                       for merkki_ARVO in 일치[0])
    return tunnus_ARVO_eb540501.sub(KORVAA_ARVO, lähdetiedosto)

def Suorita_komento():
    jäsennin_48ee4b1b = argparse.ArgumentParser()
    jäsennin_48ee4b1b.add_argument('원본', type=Path)
    jäsennin_48ee4b1b.add_argument('tulostuspaikka', type=Path)
    argumentit = jäsennin_48ee4b1b.parse_args()
    for tiedoston_nimi in sorted(argumentit.원본.rglob('*')):
        if tiedoston_nimi.suffix not in ('.c', '.h'):
            continue
        tulostuspaikka = argumentit.tulostuspaikka / tiedoston_nimi.relative_to(argumentit.원본)
        tulostuspaikka.parent.mkdir(parents=True, exist_ok=True)
        새원문 = MUUNNA_ARVO(tiedoston_nimi.read_text())
        if not tulostuspaikka.exists() or tulostuspaikka.read_text() != 새원문:
            tulostuspaikka.write_text(새원문)

if __name__ == '__main__':
    Suorita_komento()
