#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/zostava_C_kompilátor.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('zostava_C_kompilátor', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('zostava_C_kompilátor')
    mapovanie_VALUE = {'out': 'KR_údaje', 'builtins': '내장연산', 'header': 'Nadpis_VALUE', 'sdk': 'Development_Kit', 'build_ccompiler': 'Create_C_kompilátor', 'i': '순번', 'elf': 'spustiteľný_súbor', 'run': 'Vykonať_príkaz', 'flags': 'konfigurácia_Background_Intelligent_Transfer_Service', 'path': 'Cesta', 'p': 'údaje_pozícia', 'cc': 'C_kompilátor', 'obj': 'cieľový_súbor', 'flag': 'Nastavenia_VALUE', 'ld': '연결편집기', 'objects': 'cieľ_Súbory', 'repo': 'odkladací_priestor_cesta', 'v': '임시값', 'upstream': 'upstreamový', 'root': 'koreň_adresa', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Názov', 'includes': '포함인수'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
