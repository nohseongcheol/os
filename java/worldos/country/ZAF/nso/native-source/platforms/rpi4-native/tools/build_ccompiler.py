#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': '결과자료', 'builtins': '내장연산', 'header': 'Hlogo_boleng', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'phethagatša_taelo', 'flags': '설정비트', 'path': 'Tsejana', 'p': '자료위치', 'cc': '시언어번역기', 'obj': 'faele_ya_bobolokelo', 'flag': 'Dipeakanyo_boleng', 'ld': '연결편집기', 'objects': 'boyo_Difaele', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': '뿌리주소', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Leina', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
