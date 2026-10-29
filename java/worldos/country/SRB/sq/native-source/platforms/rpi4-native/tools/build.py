#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/ndërtoj_sistem.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('ndërtoj_sistem', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('ndërtoj_sistem')
    대응 = {'network': 'rrjet', 'BUILD': 'ndërtoj_shteg', 'ar': 'arkiv_vegël', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'font_të_dhëna', 'flags': 'konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metoda_futje', 'main': 'Ekzekuto', 'objcopy': 'objekt_skedar_konvertues', 'ROOT': 'Project_rrënjë', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Krijo_përdorues_HAPËSIRË', 'f': 'skedar_futje', 'extra': '추가영역', 'exports': 'eksportoj_tabelë', 'jobs': '빌드작업', 'run': 'zbatoj_komandë', 'path': 'POZICIONI', 'REPO': 'depo_rrënjë', 'tool': 'Mjete', 'classes': 'klasë_shteg', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbol_VALUE', 'source': '원본자료', 'name': 'Emër', 'build_network': 'Krijo_rrjet', 'font_info': 'font_informacion', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
