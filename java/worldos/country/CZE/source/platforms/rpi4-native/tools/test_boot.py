#!/usr/bin/env python3
"""기존 cesta_2 호환 vstupní_bod. skutečný_data implementace: ../nástroje/부팅시험.py"""
import importlib as VZÍT_HODNOTA
import sys as operační_systém_HODNOTA
from pathlib import Path as cesta_2
operační_systém_HODNOTA.path.insert(0, str(cesta_2(__file__).resolve().parents[1] / 'nástroje'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    implementace = VZÍT_HODNOTA.import_module('부팅시험')
    대응 = {'timeout': 'spuštění_TIMEOUT', 'response': 'odpověď', 'msg': 'síť_e_mail', 'exact': 'STEJNÉ_HODNOTA', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Spustit', 'cancel': 'Zrušit_operace', 'cmd_byte': 'příkaz_bajt', 'reply': 'odezva', 'points': '지점들', 'server': 'server_HODNOTA', 'data': 'data', 'prompt': 'výzva', 'enter': 'zadat', 'imported': '들여온파일', 'send': 'poslat', 'main': 'Spustit_2', 'ROOT': 'akce_kořen', 'text': 'text', 'first_gui': '첫화면', 'pixel': 'pixel', 'java_class': '자바클래스', 'upload': 'Upload_Files', 'pixels_file': 'pixel_Soubor', 'pixels_data': 'pixel_data', 'edit': 'úprava_HODNOTA', 'receive_until': '표시까지받기', 'selector': 'selektor', 'size': 'Velikost', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SEKUNDA_grafické_rozhraní_GUI', 'y': 'Y_souřadnice', 'result': 'VÝSLEDEK', 'samples': '예제들', 'client': 'klient', 'line': 'vstupní_řádek', 'report': 'ověření_Zpráva', 'work': '작업경로', 'x': 'souřadnice_x', 'python_checks': '파이썬검사', 'download': 'stažení', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'konečný_termín_ČAS', 'proc': 'Proces', 'content': 'Obsah_HODNOTA', 'block': 'datový_blok', 'marker': 'značka', 'command': 'příkaz', 'expected': '예상결과', 'shell': 'prostředí', 'drawing': 'kreslení_cesta', 'f': 'Soubor_položka', 'transcript': 'přepis', 'offset': 'POSUN_HODNOTA', 'path': 'cesta_2', 'screenshot': 'screenshot', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'výstup', 'stream': 'tok_HODNOTA', 'cmd': '명령인수', 'name': 'Název', 'qmp': '모의제어접속'}
    for Předchozí_zboží, dobrá_zboží in 대응.items():
        if hasattr(implementace, dobrá_zboží): globals()[Předchozí_zboží] = getattr(implementace, dobrá_zboží)
