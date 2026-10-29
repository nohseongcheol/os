#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/teszt_Asztal.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('teszt_Asztal', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('teszt_Asztal')
    leképezés_ÉRTÉK = {'x': 'x_koordináta', 'typing': '글자입력', 'message': 'alapelv_SMS', 'start': 'Futtatás', 'down': '누르는중', 'exact': 'AZONOS_ÉRTÉK', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'szimbólum', 'j': '안쪽순번', 'deadline': 'határidő_IDŐ', 'proc': 'Folyamat', 'data': 'adat', 'main': 'Futtatás', 'w': '너비값', 'init': '초기값', 'block': 'adatblokk', 'ROOT': 'teendő_gyök', 'text': 'Szöveg', 'marker': 'jelölő', 'report': 'ellenőrzés_jelent', 'until': '까지', 'clipboard': 'vágólap_ÉRTÉK', 'dst': 'cél_CÍM_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'átirat', 'port': 'portszám', 'offset': 'Ofszet_ÉRTÉK', 'h': '높이값', 'src': '원본주소', 'event': 'Esemény', 'encoding': 'karakterkészlet', 'size': 'Méret', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordináta', 'output': 'kimenet', 'symbol': 'szimbólum_ÉRTÉK', 'client': 'kliens', 'char': 'karakteres_adat', 'rgb': '빛삼원색'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
