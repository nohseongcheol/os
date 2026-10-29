#!/usr/bin/env python3
"""기존 ÚTVONAL 호환 belépési_pont. tényleges_adat 구현: ../Eszközök/Asztal_Nézet.py"""
import importlib as ÁTHELYEZ_ÉRTÉK
import sys as operációs_rendszer_ÉRTÉK
from pathlib import Path as ÚTVONAL
operációs_rendszer_ÉRTÉK.path.insert(0, str(ÚTVONAL(__file__).resolve().parents[1] / 'Eszközök'))
if __name__ == '__main__':
    import runpy as app_indító
    app_indító.run_module('Asztal_Nézet', run_name='__main__', alter_sys=True)
else:
    구현 = ÁTHELYEZ_ÉRTÉK.import_module('Asztal_Nézet')
    leképezés_ÉRTÉK = {'count': 'bejegyzés_DARAB', 'special': '특수글쇠', 'error': 'HIBA', 'exact': 'AZONOS_ÉRTÉK', 'network': 'hálózat', 'closed': 'informatikai_részleg_lezárt', 'length': 'hossz_ÉRTÉK', 'opened': '열림', 'ftp_port': 'fájlátvitel_portszám', 'server': 'kiszolgáló_ÉRTÉK', 'resources': 'Források', 'data': 'adat', 'shift': 'SHIFT_billentyű', 'send': 'küld', 'run_desktop': 'futtat_Asztal', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'gazda', 'text': 'Szöveg', 'korean': '한글여부', 'port': 'portszám', 'signum': 'jelzés_szám', 'version': 'verziószám', 'parser': 'elemző', 'bridge': 'híd', 'kind': 'terület_ÉRTÉK', 'tail': '끝부분', 'size': 'Méret', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordináta', 'prefix': 'sorköz_rész', 'client': 'kliens', 'char': 'karakteres_adat', 'work': '작업경로', 'Keyboard': 'billentyűzet', 'x': 'x_koordináta', 'down': '누르는중', 'net': 'híd_bejegyzés', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argumentum_TÖMB', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Folyamat', 'Desktop': 'KAPCSOLAT_Asztal', 'buttons': '단추들', 'thread': 'dolgozó', 'pressed': '눌림', 'previous': 'Előző', 'toggle': 'vált_mód', 'command': 'Parancs', 'sock': 'szoftvercsatorna_ÉRTÉK', 'frame': 'végrehajtás_doboz', 'ctrl': 'CTRL', 'path': 'ÚTVONAL', 'cp': 'karakterkódolás', 'terminate': 'leállít', 'security': 'Biztonság', 'vnc_port': '원격화면접속번호', 'body': 'törzsszöveg', 'index': 'KERES_INDEX', 'exited': '종료됨', 'keysym': 'Kulcs_szimbólum', 'output': 'kimenet', 'keyboard': 'billentyűzet_bejegyzés', 'interrupted': '가로채기됨', 'listener': 'fogad_port', 'reader': 'Olvasó', 'NetworkBridge': 'híd_3de4fe3a', 'gui': '그림화면', 'worker': 'feldolgozás_teendő'}
    for Előző_cikk, aktuális_cikk in leképezés_ÉRTÉK.items():
        if hasattr(구현, aktuális_cikk): globals()[Előző_cikk] = getattr(구현, aktuális_cikk)
