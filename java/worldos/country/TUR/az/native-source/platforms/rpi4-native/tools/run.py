#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/icra_etmək_əmr.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('icra_etmək_əmr', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('icra_etmək_əmr')
    대응 = {'supported': '지원목록', 'parser': 'parser', 'qemu': '모의기계', 'run_desktop': 'icra_iş_masası', 'main': 'İcra_Et', 'host': 'host', 'status': 'vəziyyət_VALUE', 'NetworkBridge': 'Şəbəkə_körpü', 'ROOT': 'Project_kök', 'bridge': 'körpü', 'loader': '적재기', 'base': 'Fon_VALUE', 'options': 'Seçimlər', 'binary': 'ikili', 'args': 'arqument_ARRAY', 'command': 'Əmr'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
