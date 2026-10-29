#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/teszt_felület.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('teszt_felület', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('teszt_felület')
    leképezés_ÉRTÉK = {'timeout': 'végrehajtás_IDŐTÚLLÉPÉS', 'x': 'x_koordináta', 'msg': 'hálózat_e_mail', 'i': '순번', 'reply': 'válasz', 'call': '호출', 'args': 'argumentum_TÖMB', 'chunk': '조각', 'data': 'adat', 'proc': 'Folyamat', 'long_text': '긴글', 'restored': '복원자료', 'send': 'küld', 'file': 'Fájl', 'main': 'Futtatás', 'found': 'keres_KR', 'ROOT': 'teendő_gyök', 'text': 'Szöveg', 'marker': 'jelölő', 'command': 'Parancs', 'expected': '예상결과', 'pixel': 'képpont', 'shell': 'felület', 'poll': '준비살피미', 'transcript': 'átirat', 'end': 'megszüntet_Ofszet', 'image': 'KÉP', 'key': '누름값', 'y': 'Y_koordináta', 'output': 'kimenet', 'result': 'KR', 'client': 'kliens', 'line': 'Vonal', 'stream': 'Stream_ÉRTÉK', 'name': 'Név', 'value': 'ÉRTÉK', 'receive': 'fogad_e_mail', 'report': 'ellenőrzés_jelent', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
