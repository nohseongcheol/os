#!/usr/bin/env python3
"""명시한 χρήστης ELF만 Ανάγνωση 전용 JKAP 묶음에 넣는다. 기존 디스크는 사용하지 않는다."""
import argparse
from pathlib import Path
import re
import struct

def συνδέω_τελικό_σημείο_bbe6b410():
    ανάλυση_τιμή_7cebddfb = argparse.ArgumentParser()
    ανάλυση_τιμή_7cebddfb.add_argument('-o', required=True)
    ανάλυση_τιμή_7cebddfb.add_argument('files', nargs='+', help='Όνομα=ELF경로')
    παράμετρος_όρισμα = ανάλυση_τιμή_7cebddfb.parse_args()
    if len(παράμετρος_όρισμα.files) > 32:
        ανάλυση_τιμή_7cebddfb.error('εφαρμογή_f5044b9b 최대 32개')
    항목들 = []
    이름들 = set()
    for καταχώρηση_τιμή in παράμετρος_όρισμα.files:
        Όνομα, ΔΙΑΔΡΟΜΗ = καταχώρηση_τιμή.split('=', 1)
        if not re.fullmatch('[a-z][a-z0-9_-]{0,14}', Όνομα) or Όνομα in 이름들:
            ανάλυση_τιμή_7cebddfb.error('εκτελώ_εντολή 이름이 잘못되었거나 중복됨: ' + Όνομα)
        이름들.add(Όνομα)
        δεδομένα = Path(ΔΙΑΔΡΟΜΗ).read_bytes()
        if len(δεδομένα) > 2 * 1024 * 1024:
            ανάλυση_τιμή_7cebddfb.error('εκτελώ_εντολή 파일이 너무 큼')
        항목들.append((Όνομα.encode(), δεδομένα))
    μέτρηση = bytearray(8 + 24 * len(항목들))
    struct.pack_into('<II', μέτρηση, 0, 0x50414b4a, len(항목들))
    for Ευρετήριο, (Όνομα, δεδομένα) in enumerate(항목들):
        μέτρηση.extend(bytes((-len(μέτρηση)) % 16))
        struct.pack_into('<16sII', μέτρηση, 8 + Ευρετήριο * 24, Όνομα, len(μέτρηση), len(δεδομένα))
        μέτρηση.extend(δεδομένα)
    Path(παράμετρος_όρισμα.o).write_bytes(μέτρηση)

if __name__ == '__main__':
    συνδέω_τελικό_σημείο_bbe6b410()
