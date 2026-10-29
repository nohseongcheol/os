#!/usr/bin/env python3
"""기존 ΔΙΑΔΡΟΜΗ 호환 σημείο_εισόδου. πραγματικός_δεδομένα 구현: ../Εργαλεία/εκτελώ_εντολή.py"""
import importlib as 가져오기
import sys as λειτουργικό_σύστημα_τιμή
from pathlib import Path as ΔΙΑΔΡΟΜΗ
λειτουργικό_σύστημα_τιμή.path.insert(0, str(ΔΙΑΔΡΟΜΗ(__file__).resolve().parents[1] / 'Εργαλεία'))
if __name__ == '__main__':
    import runpy as εφαρμογή_εκκίνηση
    εφαρμογή_εκκίνηση.run_module('εκτελώ_εντολή', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('εκτελώ_εντολή')
    αντιστοίχιση_τιμή = {'supported': '지원목록', 'parser': 'ανάλυση', 'qemu': '모의기계', 'run_desktop': 'εκτελώ_υπολογιστής', 'main': 'Εκτέλεση_2', 'host': 'φιλοξενώ', 'status': 'Κατάσταση_τιμή', 'NetworkBridge': 'γέφυρα_3de4fe3a', 'ROOT': 'έργο_ρίζα', 'bridge': 'γέφυρα', 'loader': 'πρόγραμμα_φόρτωσης', 'base': 'φόντο_τιμή', 'options': 'Επιλογές', 'binary': 'δυαδικός', 'args': 'όρισμα_πίνακας', 'command': 'Εντολή'}
    for 이전, τρέχων_στοιχείο in αντιστοίχιση_τιμή.items():
        if hasattr(구현, τρέχων_στοιχείο): globals()[이전] = getattr(구현, τρέχων_στοιχείο)
