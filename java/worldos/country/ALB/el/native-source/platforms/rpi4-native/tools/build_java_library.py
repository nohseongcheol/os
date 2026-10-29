#!/usr/bin/env python3
"""기존 ΔΙΑΔΡΟΜΗ 호환 σημείο_εισόδου. πραγματικός_δεδομένα 구현: ../Εργαλεία/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as λειτουργικό_σύστημα_τιμή
from pathlib import Path as ΔΙΑΔΡΟΜΗ
λειτουργικό_σύστημα_τιμή.path.insert(0, str(ΔΙΑΔΡΟΜΗ(__file__).resolve().parents[1] / 'Εργαλεία'))
if __name__ == '__main__':
    import runpy as εφαρμογή_εκκίνηση
    εφαρμογή_εκκίνηση.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    αντιστοίχιση_τιμή = {'header': 'κεφαλίδα_τιμή', 'sources': '원문목록', 'i': '순번', 'info': 'Πληροφορίες_συστήματος', 'payload': 'ωφέλιμο_φορτίο_δεδομένα', 'src': '원본주소', 'run': 'εκτελώ_εντολή', 'build_java_library': '자바라이브러리만들기', 'relative': 'σχετική_διαδρομή', 'classes': 'Τάξη_διαδρομή', 'dist': '배포경로', 'archive': 'Αρχειοθήκη', 'output': '출력결과', 'root': 'ρίζα_διεύθυνση', 'name': 'Όνομα', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, τρέχων_στοιχείο in αντιστοίχιση_τιμή.items():
        if hasattr(구현, τρέχων_στοιχείο): globals()[이전] = getattr(구현, τρέχων_στοιχείο)
