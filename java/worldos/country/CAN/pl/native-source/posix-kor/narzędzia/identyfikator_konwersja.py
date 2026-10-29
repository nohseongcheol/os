#!/usr/bin/env python3
"""polski C 식별자만 UCN으로 옮긴다. ciąg_WARTOŚĆ·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

token_WARTOŚĆ = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<identyfikator_WARTOŚĆ>[^\W\d]\w*)', re.S | re.M)

def KONWERTUJ_WARTOŚĆ(plik_źródłowy):
    def ZASTĄP_WARTOŚĆ(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(znak_WARTOŚĆ if ord(znak_WARTOŚĆ) < 128 else
                       ('\\u%04x' if ord(znak_WARTOŚĆ) <= 65535 else '\\U%08x') % ord(znak_WARTOŚĆ)
                       for znak_WARTOŚĆ in 일치[0])
    return token_WARTOŚĆ.sub(ZASTĄP_WARTOŚĆ, plik_źródłowy)

def Wykonaj_polecenie():
    parser_48ee4b1b = argparse.ArgumentParser()
    parser_48ee4b1b.add_argument('원본', type=Path)
    parser_48ee4b1b.add_argument('pozycja_wyjścia', type=Path)
    argumenty = parser_48ee4b1b.parse_args()
    for nazwa_pliku in sorted(argumenty.원본.rglob('*')):
        if nazwa_pliku.suffix not in ('.c', '.h'):
            continue
        pozycja_wyjścia = argumenty.pozycja_wyjścia / nazwa_pliku.relative_to(argumenty.원본)
        pozycja_wyjścia.parent.mkdir(parents=True, exist_ok=True)
        새원문 = KONWERTUJ_WARTOŚĆ(nazwa_pliku.read_text())
        if not pozycja_wyjścia.exists() or pozycja_wyjścia.read_text() != 새원문:
            pozycja_wyjścia.write_text(새원문)

if __name__ == '__main__':
    Wykonaj_polecenie()
