#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/부팅시험.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('부팅시험')
    mapowanie_WARTOŚĆ = {'timeout': 'wykonanie_TIMEOUT', 'response': 'odpowiedź_1262b476', 'msg': 'sieć_e_mail', 'exact': 'PORÓWNAJ_WARTOŚĆ', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Uruchom', 'cancel': 'Anuluj_zabieg', 'cmd_byte': 'polecenie_bajt', 'reply': 'odpowiedź', 'points': '지점들', 'server': 'serwer_WARTOŚĆ', 'data': 'dane', 'prompt': 'monit', 'enter': 'wprowadzić', 'imported': '들여온파일', 'send': 'wysłać', 'main': 'Uruchom_2', 'ROOT': 'Project_korzeń', 'text': 'tekst', 'first_gui': '첫화면', 'pixel': 'piksel', 'java_class': '자바클래스', 'upload': 'Upload_Files', 'pixels_file': 'piksel_Plik', 'pixels_data': 'piksel_dane', 'edit': 'Edytuj_WARTOŚĆ', 'receive_until': '표시까지받기', 'selector': 'selektor', 'size': 'Rozmiar', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SEKUNDA_GUI', 'y': 'Y_współrzędna', 'result': 'WYNIK', 'samples': '예제들', 'client': 'klient', 'line': 'wiersz_wejścia', 'report': 'walidacja_Raport', 'work': '작업경로', 'x': 'współrzędna_X', 'python_checks': '파이썬검사', 'download': 'pobrać', 'greeting': '인사', 'dims': '치수', 'chunk': 'fragment_WARTOŚĆ_652d4b53', 'deadline': 'termin_ostateczny_CZAS', 'proc': 'Proces', 'content': 'treść_WARTOŚĆ_cb0f2404', 'block': 'blok_danych', 'marker': 'pisak', 'command': 'polecenie', 'expected': '예상결과', 'shell': 'powłoka', 'drawing': 'rysunek_ścieżka', 'f': 'Plik_wpis', 'transcript': 'transkrypcja', 'offset': 'przesunąć_WARTOŚĆ_450fc799', 'path': 'ścieżka_2', 'screenshot': 'zrzut_ekranu', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'produkt_wyjściowy', 'stream': 'Stream_WARTOŚĆ', 'cmd': '명령인수', 'name': 'Nazwa', 'qmp': '모의제어접속'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
