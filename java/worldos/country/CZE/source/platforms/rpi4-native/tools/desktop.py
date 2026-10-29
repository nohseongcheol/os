#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/Plocha_pohled.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('Plocha_pohled', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('Plocha_pohled')
    대응 = {'count': 'položka_POČET', 'special': '특수글쇠', 'error': 'chyba', 'exact': 'STEJNÉ_HODNOTA', 'network': 'síť', 'closed': 'informační_systémy_uzavřeno', 'length': 'délka_HODNOTA', 'opened': '열림', 'ftp_port': 'přenos_souborů_číslo_portu', 'server': 'server_HODNOTA', 'resources': 'Prostředky', 'data': 'data', 'shift': 'klávesa_Shift', 'send': 'poslat', 'run_desktop': 'spustit_Plocha', 'protocol': 'síť_ABI', 'forwards': '전달규칙들', 'host': 'hostit', 'text': 'text', 'korean': '한글여부', 'port': 'číslo_portu', 'signum': 'signál_číslo', 'version': 'číslo_verze', 'parser': 'analyzátor', 'bridge': 'most', 'kind': 'oblast_HODNOTA', 'tail': '끝부분', 'size': 'Velikost', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_souřadnice', 'prefix': 'řádkování_část', 'client': 'klient', 'char': 'textová_data', 'work': '작업경로', 'Keyboard': 'klávesnice', 'x': 'souřadnice_x', 'down': '누르는중', 'net': 'most_položka', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argument_pole', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Proces', 'Desktop': 'spojit_Plocha', 'buttons': '단추들', 'thread': 'pracovník', 'pressed': '눌림', 'previous': 'Předchozí', 'toggle': 'SWITCH_MODE', 'command': 'příkaz', 'sock': 'soket_HODNOTA', 'frame': 'spuštění_rámec', 'ctrl': 'CTRL', 'path': 'cesta_2', 'cp': 'kódování_znaků', 'terminate': 'ukončit', 'security': 'Zabezpečení', 'vnc_port': '원격화면접속번호', 'body': 'základní_text', 'index': 'VYHLEDAT_INDEX', 'exited': '종료됨', 'keysym': 'Klíč_symbol', 'output': 'výstup', 'keyboard': 'klávesnice_položka', 'interrupted': '가로채기됨', 'listener': 'dostat_port', 'reader': 'Čtenář', 'NetworkBridge': 'most_3de4fe3a', 'gui': '그림화면', 'worker': 'zpracování_úkol'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
