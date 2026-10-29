#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/végrehajt_Fájl.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('végrehajt_Fájl', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('végrehajt_Fájl')
    leképezés_ÉRTÉK = {'timeout': 'végrehajtás_IDŐTÚLLÉPÉS', 's': 'sztring_adat', 'i': '순번', 'match': '일치', 'files': 'fájllista', 'program': 'app', 'executable': 'végrehajtható_KÉP', 'args': 'argumentum_TÖMB', 'chunk': '조각', 'data': 'adat', 'proc': 'Folyamat', 'send': 'küld', 'main': 'Futtatás', 'marker': 'jelölő', 'command': 'Parancs', 'include': 'tartalmaz', 'dumped': '갈무리자료', 'run': 'végrehajt_parancs', 'p': 'adat_pozíció', 'parser': 'elemző', 'options': 'Beállítások_7f769d16', 'kind': 'terület_ÉRTÉK', 'selector': 'szelektor', 'upload_data': 'feltölt_adat', 'end': 'megszüntet_Ofszet', 'n': 'cikk_DARAB', 'd': 'cél_adat', 'key': '누름값', 'output': 'kimenet', 'line': 'Vonal', 'name': 'Név', 'upload_name': 'feltölt_név', 'receive': 'fogad_e_mail'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
