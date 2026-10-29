#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': '결과자료', 'builtins': '내장연산', 'header': 'setlhogo_Boleng', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'diragatsa_Taelo', 'flags': '설정비트', 'path': 'tsela', 'p': '자료위치', 'cc': '시언어번역기', 'obj': 'Faele_ya_bogorogelo', 'flag': 'Diseting_Boleng', 'ld': '연결편집기', 'objects': 'bogorogelo_Difaele', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': '뿌리주소', 'assets': '탑재자료', 'source': '원본자료', 'name': 'leina', 'includes': '포함인수'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
