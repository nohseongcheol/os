#!/usr/bin/env python3
"""기존 CEĻŠ 호환 ieejas_punkts. faktisks_dati 구현: ../Rīki/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as operētājsistēma_VALUE
from pathlib import Path as CEĻŠ
operētājsistēma_VALUE.path.insert(0, str(CEĻŠ(__file__).resolve().parents[1] / 'Rīki'))
if __name__ == '__main__':
    import runpy as programma_palaidējs
    programma_palaidējs.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    kartēšana_VALUE = {'timeout': '시간제한', 'response': 'atbilde_1262b476', 'msg': 'tīkls_ziņa', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Izpildīt', 'cancel': 'Atcelt_operācija', 'cmd_byte': 'komanda_byte', 'reply': 'atbilde', 'points': '지점들', 'server': 'serveris_VALUE', 'data': 'dati', 'prompt': 'uzvedne', 'enter': 'ievadīt', 'imported': '들여온파일', 'send': 'sūtīt', 'main': 'Palaist', 'ROOT': 'Project_sakne', 'text': 'Teksts', 'first_gui': '첫화면', 'pixel': 'attēla_elements', 'java_class': '자바클래스', 'upload': 'Upload_Faili', 'pixels_file': 'attēla_elements_Fails', 'pixels_data': 'attēla_elements_dati', 'edit': 'Rediģēt_VALUE', 'receive_until': '표시까지받기', 'selector': 'atlasītājs', 'size': 'Izmērs', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'mērs', 'samples': '예제들', 'client': 'klients', 'line': 'Līniju', 'report': 'validācija_ziņot', 'work': '작업경로', 'x': 'x_koordināta', 'python_checks': '파이썬검사', 'download': 'lejupielāde', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'izpildes_termiņš_TIME', 'proc': 'Process', 'content': 'Saturs_VALUE', 'block': 'datu_bloks', 'marker': 'marķieris', 'command': 'Komanda', 'expected': '예상결과', 'shell': 'čaula', 'drawing': 'zīmējums_ceļš', 'f': 'Fails_ievade', 'transcript': 'transkripcija', 'offset': 'Nobīde_VALUE', 'path': 'CEĻŠ', 'screenshot': 'ekrānuzņēmums', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'ražojums', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'Nosaukums', 'qmp': '모의제어접속'}
    for 이전, pašreizējais_krājums in kartēšana_VALUE.items():
        if hasattr(구현, pašreizējais_krājums): globals()[이전] = getattr(구현, pašreizējais_krājums)
