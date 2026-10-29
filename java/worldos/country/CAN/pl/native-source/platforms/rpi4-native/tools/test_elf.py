#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/실행파일시험.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('실행파일시험')
    mapowanie_WARTOŚĆ = {'out': 'KR_dane', 'expected': '예상결과', 'phoff': 'program_Nagłówek_przesunąć', 'offset': 'przesunąć_WARTOŚĆ_450fc799', 'invalid': 'nieważny_dane', 'path': 'ścieżka_2', 'executable': 'wykonywalny_OBRAZ', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'WYNIK', 'format_': 'format_b87fd068', 'main': 'Uruchom_2', 'content': 'treść_WARTOŚĆ_cb0f2404', 'source': '원본자료', 'name': 'Nazwa', 'reference': 'Porównanie_plan_bazowy', 'ROOT': 'Project_korzeń', 'value': 'WARTOŚĆ', 'report': 'walidacja_Raport'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
