#!/usr/bin/env python3
"""기존 ΔΙΑΔΡΟΜΗ 호환 σημείο_εισόδου. πραγματικός_δεδομένα 구현: ../Εργαλεία/ανεβάζω_Αρχεία.py"""
import importlib as 가져오기
import sys as λειτουργικό_σύστημα_τιμή
from pathlib import Path as ΔΙΑΔΡΟΜΗ
λειτουργικό_σύστημα_τιμή.path.insert(0, str(ΔΙΑΔΡΟΜΗ(__file__).resolve().parents[1] / 'Εργαλεία'))
if __name__ == '__main__':
    import runpy as εφαρμογή_εκκίνηση
    εφαρμογή_εκκίνηση.run_module('ανεβάζω_Αρχεία', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ανεβάζω_Αρχεία')
    αντιστοίχιση_τιμή = {'data': 'δεδομένα', 'i': '순번', 'name': 'Όνομα', 'c': 'σημείο_κώδικα', 'p': 'δεδομένα_θέση', 'args': 'όρισμα_πίνακας'}
    for 이전, τρέχων_στοιχείο in αντιστοίχιση_τιμή.items():
        if hasattr(구현, τρέχων_στοιχείο): globals()[이전] = getattr(구현, τρέχων_στοιχείο)
