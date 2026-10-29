#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/phethagatša_faele.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('phethagatša_faele', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('phethagatša_faele')
    대응 = {'timeout': '시간제한', 's': 'molokoloko_data', 'i': '순번', 'match': '일치', 'files': 'faele_Lenaneo', 'program': 'tirišo', 'executable': '실행가능파일', 'args': 'akumente_arei', 'chunk': '조각', 'data': 'data', 'proc': 'tiragalo_a7054519', 'send': 'Romela', 'main': 'Diriša', 'marker': '확인표시', 'command': 'Taelo', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'phethagatša_taelo', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Dikgetho', 'kind': 'legoro_boleng', 'selector': 'sekgethi', 'upload_data': 'apolouto_data', 'end': 'fetša_E_Šetšego', 'n': '개수', 'd': 'boyo_data', 'key': '누름값', 'output': '출력결과', 'line': 'mothaladi', 'name': 'Leina', 'upload_name': 'apolouto_leina', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
