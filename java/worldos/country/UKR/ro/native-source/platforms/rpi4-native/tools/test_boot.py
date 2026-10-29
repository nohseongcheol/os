#!/usr/bin/env python3
"""기존 Cale 호환 intrare_p. real_date 구현: ../Instrumente/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as sistem_de_operare_VALUE
from pathlib import Path as Cale
sistem_de_operare_VALUE.path.insert(0, str(Cale(__file__).resolve().parents[1] / 'Instrumente'))
if __name__ == '__main__':
    import runpy as program_ecrane_de_lansare
    program_ecrane_de_lansare.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    mapare_VALUE = {'timeout': 'executare_TIMEOUT', 'response': 'răspuns', 'msg': 'rețea_mesaj', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Execută', 'cancel': 'anula_operație', 'cmd_byte': 'comandă_byte', 'reply': 'replică', 'points': '지점들', 'server': 'server_VALUE', 'data': 'date', 'prompt': 'solicita', 'enter': 'introduce', 'imported': '들여온파일', 'send': 'trimite', 'main': 'Pornește', 'ROOT': 'Project_rădăcină', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'element_imagine', 'java_class': '자바클래스', 'upload': 'Upload_Fișiere', 'pixels_file': 'element_imagine_Fișier', 'pixels_data': 'element_imagine_date', 'edit': 'edita_VALUE', 'receive_until': '표시까지받기', 'selector': 'selector', 'size': 'Mărime', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'KR', 'samples': '예제들', 'client': 'client', 'line': 'Linie', 'report': 'validare_raport', 'work': '작업경로', 'x': 'coordonata_X', 'python_checks': '파이썬검사', 'download': 'descărca', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'dată_limită_oră', 'proc': 'Proces', 'content': 'Conținut_VALUE', 'block': 'bloc_de_date', 'marker': 'marcaj', 'command': 'Comandă', 'expected': '예상결과', 'shell': 'shell', 'drawing': 'desen_cale', 'f': 'Fișier_intrare', 'transcript': 'transcriere', 'offset': 'OFFSET_VALUE', 'path': 'Cale', 'screenshot': 'captură_de_ecran', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'flux_VALUE', 'cmd': '명령인수', 'name': 'Nume', 'qmp': '모의제어접속'}
    for Anteriorul_element, curent_element in mapare_VALUE.items():
        if hasattr(구현, curent_element): globals()[Anteriorul_element] = getattr(구현, curent_element)
