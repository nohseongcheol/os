#!/usr/bin/env python3
"""기존 POZICIONI 호환 futje_p. aktual_të_dhëna 구현: ../Mjete/ndërtoj_përdorues_HAPËSIRË.py"""
import importlib as TAKE_VALUE
import sys as sistem_operativ_VALUE
from pathlib import Path as POZICIONI
sistem_operativ_VALUE.path.insert(0, str(POZICIONI(__file__).resolve().parents[1] / 'Mjete'))
if __name__ == '__main__':
    import runpy as program_hapës
    program_hapës.run_module('ndërtoj_përdorues_HAPËSIRË', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('ndërtoj_përdorues_HAPËSIRË')
    대응 = {'mode': 'metoda_MODE', 'header': 'Kreu_VALUE', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'arkiv_vegël', 'posix': '포직스경로', 'payload': 'ngarkesë_e_dobishme_të_dhëna', 'flags': 'konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'të_dhëna', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'depo_shteg', 'build_python': 'Krijo_PYTHON', 'inc': '포함경로', 'argument': '전달값', 'text': 'Teksti', 'headers': 'Kreu_Listë', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'ndërtoj', 'build_users': 'Krijo_përdorues_HAPËSIRË', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'program_Kreu_OFFSET', 'offset': 'OFFSET_VALUE', 'text_address': 'komandë_email', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'zbatoj_komandë', 'path': 'POZICIONI', 'p': 'të_dhëna_pozicioni', 'changed': '바뀐자료', 'n': 'njësi_COUNT', 'flag': 'cilësimet_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'klasë_shteg', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'të_dhëna_email', 'symbol': 'simbol_VALUE', 'root': 'rrënjë_email', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Emër', 'value': 'VALUE', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
