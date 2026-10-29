#!/usr/bin/env python3
"""ελληνικά C 식별자만 UCN으로 옮긴다. συμβολοσειρά_τιμή·문자·주석·include 파일명은 보존한다."""
import argparse
from pathlib import Path
import re

διακριτικό_τιμή = re.compile(r'(?P<보존>//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|^[ \t]*#[ \t]*include[ \t]*<[^>]*>)|(?P<αναγνωριστικό_τιμή>[^\W\d]\w*)', re.S | re.M)

def μετατρέπω_τιμή(ΠΗΓΗ):
    def αντικαθιστώ_τιμή(일치):
        if 일치.lastgroup == '보존':
            return 일치[0]
        return ''.join(χαρακτήρας_τιμή if ord(χαρακτήρας_τιμή) < 128 else
                       ('\\u%04x' if ord(χαρακτήρας_τιμή) <= 65535 else '\\U%08x') % ord(χαρακτήρας_τιμή)
                       for χαρακτήρας_τιμή in 일치[0])
    return διακριτικό_τιμή.sub(αντικαθιστώ_τιμή, ΠΗΓΗ)

def εκτελώ_εντολή():
    ανάλυση_48ee4b1b = argparse.ArgumentParser()
    ανάλυση_48ee4b1b.add_argument('원본', type=Path)
    ανάλυση_48ee4b1b.add_argument('Έξοδος', type=Path)
    Παράμετροι = ανάλυση_48ee4b1b.parse_args()
    for Αρχείο in sorted(Παράμετροι.원본.rglob('*')):
        if Αρχείο.suffix not in ('.c', '.h'):
            continue
        Έξοδος = Παράμετροι.Έξοδος / Αρχείο.relative_to(Παράμετροι.원본)
        Έξοδος.parent.mkdir(parents=True, exist_ok=True)
        새원문 = μετατρέπω_τιμή(Αρχείο.read_text())
        if not Έξοδος.exists() or Έξοδος.read_text() != 새원문:
            Έξοδος.write_text(새원문)

if __name__ == '__main__':
    εκτελώ_εντολή()
