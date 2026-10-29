#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/aga_lenaneo.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('aga_lenaneo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('aga_lenaneo')
    대응 = {'network': 'Netweke', 'BUILD': 'aga_tsela', 'ar': 'Akhaebe_tholosi', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'fonte_data', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'akumente_arei', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'mokgwa_go_tsenya_tshedimošo', 'main': 'Diriša', 'objcopy': 'selo_faele_sefetošetši', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': '사용자영역만들기', 'f': 'faele_go_tsenya_tshedimošo', 'extra': '추가영역', 'exports': 'Iša_tafola', 'jobs': '빌드작업', 'run': 'phethagatša_taelo', 'path': 'Tsejana', 'REPO': '저장소', 'tool': 'Ditholosi', 'classes': 'legoro_tsela', 'output': '출력결과', 'samples': '예제들', 'symbol': 'leswao_boleng', 'source': '원본자료', 'name': 'Leina', 'build_network': '통신망만들기', 'font_info': 'fonte_tshedimošo', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
