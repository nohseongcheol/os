#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/generare_sistem.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('generare_sistem', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('generare_sistem')
    mapare_VALUE = {'network': 'rețea', 'BUILD': 'generare_cale', 'ar': 'Arhivă_instrument', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'font_date', 'flags': 'configurație_Serviciu_de_transfer_inteligent_în_fundal', 'a': '첫째값', 'cc': 'C_compilator', 'args': 'argument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metodă_intrare', 'main': 'Pornește', 'objcopy': 'obiect_Fișier_convertor', 'ROOT': 'Project_rădăcină', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'compilator_instrument', 'build_users': 'crea_utilizator_SPAȚIU', 'f': 'Fișier_intrare', 'extra': '추가영역', 'exports': 'exporta_tabel', 'jobs': '빌드작업', 'run': 'executa_comandă', 'path': 'Cale', 'REPO': 'depozit_rădăcină', 'tool': 'Instrumente', 'classes': 'Clasă_cale', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Nume', 'build_network': 'crea_rețea_48d29d6d', 'font_info': 'font_info', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
