#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'llogaritje_të_dhëna', 'builtins': '내장연산', 'header': 'Kreu_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'zbatoj_komandë', 'flags': 'konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond', 'path': 'POZICIONI', 'p': 'të_dhëna_pozicioni', 'cc': '시언어번역기', 'obj': 'skedari_i_vendmbërritjes', 'flag': 'cilësimet_VALUE', 'ld': '연결편집기', 'objects': 'vendmbërritje_Skedarët', 'repo': 'depo_shteg', 'v': '임시값', 'upstream': 'upstream', 'root': 'rrënjë_email', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Emër', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
