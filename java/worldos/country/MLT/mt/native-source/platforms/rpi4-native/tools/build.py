#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/bena_sistema.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('bena_sistema', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('bena_sistema')
    대응 = {'network': 'netwerk', 'BUILD': 'bena_mogħdija', 'ar': 'Arkivju_għodda', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'font_data', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'argument_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'metodu_entrata', 'main': 'serje', 'objcopy': 'oġġett_fajl_konverter', 'ROOT': 'pprojetta_għerq', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ħalaq_utent_SPACE', 'f': 'fajl_entrata', 'extra': '추가영역', 'exports': 'esporta_tabella', 'jobs': '빌드작업', 'run': 'eżegwixxa_kmand', 'path': 'mogħdija', 'REPO': '저장소', 'tool': 'Għodod', 'classes': 'klassi_mogħdija', 'output': '출력결과', 'samples': '예제들', 'symbol': 'simbolu_VALUE', 'source': '원본자료', 'name': 'isem', 'build_network': 'ħalaq_netwerk', 'font_info': 'font_informazzjoni', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
