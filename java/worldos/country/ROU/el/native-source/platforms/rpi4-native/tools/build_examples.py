#!/usr/bin/env python3
"""기존 ΔΙΑΔΡΟΜΗ 호환 σημείο_εισόδου. πραγματικός_δεδομένα 구현: ../Εργαλεία/예제빌드.py"""
import importlib as 가져오기
import sys as λειτουργικό_σύστημα_τιμή
from pathlib import Path as ΔΙΑΔΡΟΜΗ
λειτουργικό_σύστημα_τιμή.path.insert(0, str(ΔΙΑΔΡΟΜΗ(__file__).resolve().parents[1] / 'Εργαλεία'))
if __name__ == '__main__':
    import runpy as εφαρμογή_εκκίνηση
    εφαρμογή_εκκίνηση.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    αντιστοίχιση_τιμή = {'out': 'μέτρηση_δεδομένα', 'build_examples': '예제만들기', 'files': 'λίστα_αρχείων', 'java': '자바실행', 'run': 'εκτελώ_εντολή', 'path': 'ΔΙΑΔΡΟΜΗ', 'p': 'δεδομένα_θέση', 'readme': 'αρχείο_readme', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'Αναζήτηση_Ευρετήριο', 'classes': 'Τάξη_διαδρομή', 'repo': 'αποθετήριο_διαδρομή', 'root': 'ρίζα_διεύθυνση', 'content': 'Περιεχόμενο_τιμή', 'source': '원본자료', 'name': 'Όνομα', 'target': 'τιμή_στόχος', 'manifest': 'πακέτο_διακήρυξη', 'language': 'Γλώσσα'}
    for 이전, τρέχων_στοιχείο in αντιστοίχιση_τιμή.items():
        if hasattr(구현, τρέχων_στοιχείο): globals()[이전] = getattr(구현, τρέχων_στοιχείο)
