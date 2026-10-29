#!/usr/bin/env python3
"""기존 Inzira 호환 icyinjizwa_inota. nyakuri_amakurushingiro 구현: ../Ibikoresho/gusohora_sisitemu.py"""
import importlib as 가져오기
import sys as sisitemu_ngengamikorere_agaciro
from pathlib import Path as Inzira
sisitemu_ngengamikorere_agaciro.path.insert(0, str(Inzira(__file__).resolve().parents[1] / 'Ibikoresho'))
if __name__ == '__main__':
    import runpy as porogaramu_umukozi
    porogaramu_umukozi.run_module('gusohora_sisitemu', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('gusohora_sisitemu')
    대응 = {'network': 'Urusobemiyoboro', 'BUILD': 'gusohora_inzira', 'ar': 'gushyingura_igikoresho', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'imyandikire_amakurushingiro', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'ingingo_ARRAY', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'uburyo_icyinjizwa', 'main': 'ihuriro', 'objcopy': 'ikintu_dosiye_muhinduzi', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'kurema_ukoresha_akanya', 'f': 'dosiye_icyinjizwa', 'extra': '추가영역', 'exports': 'kwimura_imbonerahamwe', 'jobs': '빌드작업', 'run': 'gukora_ibwiriza', 'path': 'Inzira', 'REPO': '저장소', 'tool': 'Ibikoresho', 'classes': 'icyiciro_inzira', 'output': '출력결과', 'samples': '예제들', 'symbol': 'ikimenyetso_agaciro', 'source': '원본자료', 'name': 'Izina', 'build_network': 'kurema_Urusobemiyoboro_48d29d6d', 'font_info': 'imyandikire_amakuru', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
