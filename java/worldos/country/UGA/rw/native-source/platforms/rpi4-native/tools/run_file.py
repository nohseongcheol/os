#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/gukora_dosiye.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('gukora_dosiye', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('gukora_dosiye')
    대응 = {'timeout': '시간제한', 's': 'igicenteruro_amakurushingiro', 'i': '순번', 'match': '일치', 'files': 'dosiye_Urutonde', 'program': 'porogaramu', 'executable': '실행가능파일', 'args': 'ingingo_ARRAY', 'chunk': '조각', 'data': 'amakurushingiro', 'proc': 'Inzira_a7054519', 'send': 'kohereza', 'main': 'ihuriro', 'marker': '확인표시', 'command': 'Icyo_wifuza', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'gukora_ibwiriza', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Amahitamo', 'kind': 'icyiciro_agaciro', 'selector': 'muhitamo', 'upload_data': 'gukurura_amakurushingiro', 'end': 'kurangiza_Ofuseti', 'n': '개수', 'd': 'aho_ijya_amakurushingiro', 'key': '누름값', 'output': '출력결과', 'line': 'umurongo', 'name': 'Izina', 'upload_name': 'gukurura_izina', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
