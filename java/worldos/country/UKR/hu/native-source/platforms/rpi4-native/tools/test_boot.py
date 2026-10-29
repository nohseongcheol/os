#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/부팅시험.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('부팅시험')
    leképezés_ÉRTÉK = {'timeout': 'végrehajtás_IDŐTÚLLÉPÉS', 'response': 'válasz_1262b476', 'msg': 'hálózat_e_mail', 'exact': 'AZONOS_ÉRTÉK', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Végrehajtás', 'cancel': 'Mégse_műtét', 'cmd_byte': 'parancs_bájt', 'reply': 'válasz', 'points': '지점들', 'server': 'kiszolgáló_ÉRTÉK', 'data': 'adat', 'prompt': 'kér', 'enter': 'megad', 'imported': '들여온파일', 'send': 'küld', 'main': 'Futtatás', 'ROOT': 'teendő_gyök', 'text': 'Szöveg', 'first_gui': '첫화면', 'pixel': 'képpont', 'java_class': '자바클래스', 'upload': 'feltölt_Files', 'pixels_file': 'képpont_Fájl', 'pixels_data': 'képpont_adat', 'edit': 'szerkeszt_ÉRTÉK', 'receive_until': '표시까지받기', 'selector': 'szelektor', 'size': 'Méret', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'MPERC_vizuális_felület', 'y': 'Y_koordináta', 'result': 'KR', 'samples': '예제들', 'client': 'kliens', 'line': 'Vonal', 'report': 'ellenőrzés_jelent', 'work': '작업경로', 'x': 'x_koordináta', 'python_checks': '파이썬검사', 'download': 'letölt', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'határidő_IDŐ', 'proc': 'Folyamat', 'content': 'Tartalom_ÉRTÉK', 'block': 'adatblokk', 'marker': 'jelölő', 'command': 'Parancs', 'expected': '예상결과', 'shell': 'felület', 'drawing': 'rajz_útvonal', 'f': 'Fájl_bejegyzés', 'transcript': 'átirat', 'offset': 'Ofszet_ÉRTÉK', 'path': 'ÚTVONAL', 'screenshot': 'képernyőkép', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'kimenet', 'stream': 'Stream_ÉRTÉK', 'cmd': '명령인수', 'name': 'Név', 'qmp': '모의제어접속'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
