#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/järk_süsteem.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('järk_süsteem', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('järk_süsteem')
    vastendamine_VALUE = {'network': 'võrk', 'BUILD': 'järk_tee', 'ar': 'Arhiiv_tööriist', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'font_andmed', 'flags': 'konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus', 'a': '첫째값', 'cc': '_15_kompilaator', 'args': 'argument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'meetod_kirje', 'main': 'Käivita_2', 'objcopy': 'objekt_Fail_muundur', 'ROOT': 'Project_juur', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kompilaator_tööriist', 'build_users': 'avama_kasutaja_ruum', 'f': 'Fail_kirje', 'extra': '추가영역', 'exports': 'eksportima_tabel', 'jobs': '빌드작업', 'run': 'Täida_käsk', 'path': 'RADA', 'REPO': 'hoidla_juur', 'tool': 'Tööriistad', 'classes': 'tund_tee', 'output': 'toodang', 'samples': '예제들', 'symbol': 'sümbol_VALUE', 'source': '원본자료', 'name': 'Nimi_2', 'build_network': 'avama_võrk_48d29d6d', 'font_info': 'font_teave', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
