#!/usr/bin/env python3
"""기존 ΔΙΑΔΡΟΜΗ 호환 σημείο_εισόδου. πραγματικός_δεδομένα 구현: ../Εργαλεία/되돌림시험서버.py"""
import importlib as 가져오기
import sys as λειτουργικό_σύστημα_τιμή
from pathlib import Path as ΔΙΑΔΡΟΜΗ
λειτουργικό_σύστημα_τιμή.path.insert(0, str(ΔΙΑΔΡΟΜΗ(__file__).resolve().parents[1] / 'Εργαλεία'))
if __name__ == '__main__':
    import runpy as εφαρμογή_εκκίνηση
    εφαρμογή_εκκίνηση.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    αντιστοίχιση_τιμή = {'data': 'δεδομένα', 'e': '보조항목', 'connection': 'σύνδεση_e05f319b', 'f': 'Αρχείο_καταχώρηση', 'peer': 'ομότιμος_τιμή', 'self': '자신', 'udp': 'αυτοδύναμο_πακέτο_έλεγχος', 't': 'Τερματικό_καταχώρηση', 'tcp': 'σύνδεση_έλεγχος', 'EchoFixture': '되돌림시험서버', 'args': 'όρισμα_πίνακας', 'chunk': '조각'}
    for 이전, τρέχων_στοιχείο in αντιστοίχιση_τιμή.items():
        if hasattr(구현, τρέχων_στοιχείο): globals()[이전] = getattr(구현, τρέχων_στοιχείο)
