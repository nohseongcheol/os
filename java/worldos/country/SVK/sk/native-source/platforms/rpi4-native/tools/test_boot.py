#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    mapovanie_VALUE = {'timeout': '시간제한', 'response': 'odpoveď', 'msg': 'sieť_e_mail', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Spustiť', 'cancel': 'zrušiť_operácia', 'cmd_byte': 'príkaz_Byte', 'reply': 'odozva', 'points': '지점들', 'server': 'server_VALUE', 'data': 'údaje', 'prompt': 'výzva', 'enter': 'zadať', 'imported': '들여온파일', 'send': 'odoslať', 'main': 'Spustiť_2', 'ROOT': 'akcia_koreň', 'text': 'Spracovanie_textu', 'first_gui': '첫화면', 'pixel': 'pixel', 'java_class': '자바클래스', 'upload': 'nahrať_Súbory', 'pixels_file': 'pixel_Súbor', 'pixels_data': 'pixel_údaje', 'edit': 'úprava_VALUE', 'receive_until': '표시까지받기', 'selector': 'selektor', 'size': 'Veľkosť', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_grafické_používateľské_rozhranie', 'y': 'Y_súradnica', 'result': 'KR', 'samples': '예제들', 'client': 'klient', 'line': 'riadok', 'report': 'overenie_správa', 'work': '작업경로', 'x': 'X_súradnica', 'python_checks': '파이썬검사', 'download': 'prevziať', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'termín_čas', 'proc': 'Proces', 'content': 'obsah_VALUE', 'block': 'blok_údajov', 'marker': 'fixka', 'command': 'Príkaz', 'expected': '예상결과', 'shell': '셸', 'drawing': 'kresba_cesta', 'f': 'Súbor_položka', 'transcript': 'prepis', 'offset': 'Posun_VALUE', 'path': 'Cesta', 'screenshot': 'výrez_obrazovky', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'Názov', 'qmp': '모의제어접속'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
