#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/aga_Netweke.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('aga_Netweke', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('aga_Netweke')
    대응 = {'obj': 'faele_ya_bobolokelo', 'objects': 'boyo_Difaele', 'library': 'Bokgobadata', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'faele_Lenaneo', 'source': '원본자료', 'run': 'phethagatša_taelo', 'flags': '설정비트', 'path': 'Tsejana', 'build_network': '통신망만들기', 'cc': '시언어번역기', 'ar': 'Akhaebe_tholosi'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
