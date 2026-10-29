#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/järk_kasutaja_ruum.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('järk_kasutaja_ruum', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('järk_kasutaja_ruum')
    vastendamine_VALUE = {'mode': 'meetod_MODE', 'header': 'Päis_VALUE', 'i': '순번', 'build_ccompiler': 'avama_15_kompilaator', 'ar': 'Arhiiv_tööriist', 'posix': '포직스경로', 'payload': 'last_andmed', 'flags': 'konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus', 'cases': '시험사례', 'cc': '_15_kompilaator', 'data': 'andmed', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'hoidla_tee', 'build_python': 'avama_PYTHON', 'inc': 'hõlmama_tee', 'argument': '전달값', 'text': 'Tekst', 'headers': 'Päis_Loend', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'järk', 'build_users': 'avama_kasutaja_ruum', 'compiler': 'kompilaator_tööriist', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'programm_Päis_nihe', 'offset': 'nihe_VALUE', 'text_address': 'käsk_ADDRESS', 'abi': '호출규약', 'assembly': 'komplekt', 'run': 'Täida_käsk', 'path': 'RADA', 'p': 'andmed_ametikoht', 'changed': '바뀐자료', 'n': 'kaup_COUNT', 'flag': 'Sätted_VALUE', 'index': 'LOOKUP_INDEX', 'classes': 'tund_tee', 'output': 'toodang', 'loads': '적재구획', 'data_address': 'andmed_ADDRESS', 'symbol': 'sümbol_VALUE', 'root': 'juur_ADDRESS', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nimi_2', 'value': 'VALUE', 'fmt': 'vorming_932e03c8', 'work': '작업경로'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
