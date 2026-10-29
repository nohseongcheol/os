#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/počítač_zobraziť.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('počítač_zobraziť', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('počítač_zobraziť')
    mapovanie_VALUE = {'count': 'položka_COUNT_8f7753a1', 'special': '특수글쇠', 'error': 'chyba', 'exact': 'EXACT_VALUE', 'network': 'sieť', 'closed': '닫힘', 'length': 'dĺžka_VALUE', 'opened': '열림', 'ftp_port': 'prenos_súborov_číslo_portu', 'server': 'server_VALUE', 'resources': 'Zdroje', 'data': 'údaje', 'shift': 'kláves_Shift', 'send': 'odoslať', 'run_desktop': 'spustiť_počítač', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'hostiteľ', 'text': 'Spracovanie_textu', 'korean': '한글여부', 'port': 'číslo_portu', 'signum': '신호번호', 'version': 'číslo_verzie', 'parser': 'analyzátor', 'bridge': 'most', 'kind': 'oblasť_VALUE', 'tail': '끝부분', 'size': 'Veľkosť', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_súradnica', 'prefix': '앞부분', 'client': 'klient', 'char': 'znakové_údaje', 'work': '작업경로', 'Keyboard': 'klávesnica', 'x': 'X_súradnica', 'down': '누르는중', 'net': 'sieťový_most_položka', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_pole', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proces', 'Desktop': 'spojiť_počítač', 'buttons': '단추들', 'thread': '작업가닥', 'pressed': '눌림', 'previous': '이전항목', 'toggle': 'SWITCH_MODE', 'command': 'Príkaz', 'sock': 'soket_VALUE', 'frame': '실행틀', 'ctrl': 'kláves_CTRL', 'path': 'Cesta', 'cp': 'kódovanie_znakov', 'terminate': '종료시키기', 'security': 'Zabezpečenie', 'vnc_port': '원격화면접속번호', 'body': 'základný_text', 'index': 'LOOKUP_INDEX', 'exited': '종료됨', 'keysym': 'Kľúč_symbol', 'output': '출력결과', 'keyboard': 'klávesnica_položka', 'interrupted': '가로채기됨', 'listener': 'dostať_port', 'reader': 'Čítačka', 'NetworkBridge': 'sieťový_most', 'gui': '그림화면', 'worker': 'spracovanie_úloha'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
