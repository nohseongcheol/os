#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/gusohora_Urusobemiyoboro.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('gusohora_Urusobemiyoboro', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('gusohora_Urusobemiyoboro')
    대응 = {'obj': 'dosiye_yerekezwaho', 'objects': 'aho_ijya_Dosiye', 'library': 'isomero', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'dosiye_Urutonde', 'source': '원본자료', 'run': 'gukora_ibwiriza', 'flags': '설정비트', 'path': 'Inzira', 'build_network': 'kurema_Urusobemiyoboro_48d29d6d', 'cc': '시언어번역기', 'ar': 'gushyingura_igikoresho'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
