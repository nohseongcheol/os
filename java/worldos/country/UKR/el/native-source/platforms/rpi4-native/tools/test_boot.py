#!/usr/bin/env python3
"""기존 ΔΙΑΔΡΟΜΗ 호환 σημείο_εισόδου. πραγματικός_δεδομένα 구현: ../Εργαλεία/부팅시험.py"""
import importlib as 가져오기
import sys as λειτουργικό_σύστημα_τιμή
from pathlib import Path as ΔΙΑΔΡΟΜΗ
λειτουργικό_σύστημα_τιμή.path.insert(0, str(ΔΙΑΔΡΟΜΗ(__file__).resolve().parents[1] / 'Εργαλεία'))
if __name__ == '__main__':
    import runpy as εφαρμογή_εκκίνηση
    εφαρμογή_εκκίνηση.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    αντιστοίχιση_τιμή = {'timeout': 'εκτέλεση_ΤΕΛΟΣ_ΧΡΟΝΟΥ', 'response': 'απάντηση', 'msg': 'δίκτυο_μήνυμα', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Εκτέλεση', 'cancel': 'Άκυρο_εγχείρηση', 'cmd_byte': '명령바이트', 'reply': 'απαντώ', 'points': '지점들', 'server': 'διακομιστής_τιμή', 'data': 'δεδομένα', 'prompt': 'ζητώ', 'enter': 'εισάγω', 'imported': '들여온파일', 'send': 'στέλνω', 'main': 'Εκτέλεση_2', 'ROOT': 'έργο_ρίζα', 'text': 'Κείμενο', 'first_gui': '첫화면', 'pixel': '화소', 'java_class': '자바클래스', 'upload': 'ανεβάζω_Αρχεία', 'pixels_file': '화소파일', 'pixels_data': '화소자료', 'edit': 'Τροποποίησε_τιμή', 'receive_until': '표시까지받기', 'selector': 'επιλογέας', 'size': 'Μέγεθος', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'κουμπί_Y_συντονισμός', 'result': 'μέτρηση', 'samples': '예제들', 'client': 'πελάτης', 'line': 'Γραμμή', 'report': 'επικύρωση_έκθεση', 'work': '작업경로', 'x': 'συντεταγμένη_x', 'python_checks': '파이썬검사', 'download': 'λήψη', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'προθεσμία_ώρα', 'proc': 'Διεργασία', 'content': 'Περιεχόμενο_τιμή', 'block': 'μπλοκ_δεδομένων', 'marker': 'δείκτης_8b722c5f', 'command': 'Εντολή', 'expected': '예상결과', 'shell': 'κέλυφος', 'drawing': 'σχέδιο_διαδρομή', 'f': 'Αρχείο_καταχώρηση', 'transcript': 'μεταγραφή', 'offset': 'Υπέρθεση_τιμή', 'path': 'ΔΙΑΔΡΟΜΗ', 'screenshot': 'απόσπασμα_οθόνης', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'ροή_τιμή', 'cmd': '명령인수', 'name': 'Όνομα', 'qmp': '모의제어접속'}
    for 이전, τρέχων_στοιχείο in αντιστοίχιση_τιμή.items():
        if hasattr(구현, τρέχων_στοιχείο): globals()[이전] = getattr(구현, τρέχων_στοιχείο)
