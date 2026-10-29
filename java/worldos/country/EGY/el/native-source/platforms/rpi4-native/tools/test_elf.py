#!/usr/bin/env python3
"""기존 ΔΙΑΔΡΟΜΗ 호환 σημείο_εισόδου. πραγματικός_δεδομένα 구현: ../Εργαλεία/실행파일시험.py"""
import importlib as 가져오기
import sys as λειτουργικό_σύστημα_τιμή
from pathlib import Path as ΔΙΑΔΡΟΜΗ
λειτουργικό_σύστημα_τιμή.path.insert(0, str(ΔΙΑΔΡΟΜΗ(__file__).resolve().parents[1] / 'Εργαλεία'))
if __name__ == '__main__':
    import runpy as εφαρμογή_εκκίνηση
    εφαρμογή_εκκίνηση.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    αντιστοίχιση_τιμή = {'out': 'μέτρηση_δεδομένα', 'expected': '예상결과', 'phoff': 'εφαρμογή_κεφαλίδα_Υπέρθεση', 'offset': 'Υπέρθεση_τιμή', 'invalid': 'άκυρος_δεδομένα', 'path': 'ΔΙΑΔΡΟΜΗ', 'executable': 'εκτελέσιμο_εικόνα', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'μέτρηση', 'format_': 'μορφή_b87fd068', 'main': 'Εκτέλεση_2', 'content': 'Περιεχόμενο_τιμή', 'source': '원본자료', 'name': 'Όνομα', 'reference': 'Σύγκριση_γραμμή_βάσης', 'ROOT': 'έργο_ρίζα', 'value': 'τιμή', 'report': 'επικύρωση_έκθεση'}
    for 이전, τρέχων_στοιχείο in αντιστοίχιση_τιμή.items():
        if hasattr(구현, τρέχων_στοιχείο): globals()[이전] = getattr(구현, τρέχων_στοιχείο)
