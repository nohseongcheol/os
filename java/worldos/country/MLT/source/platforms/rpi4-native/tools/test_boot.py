#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/부팅시험.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'netwerk_messaġġ', 'exact': 'EXACT_VALUE', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'eżegwixxa_attività', 'cancel': 'kkanċella_operazzjoni', 'cmd_byte': 'kmand_byte', 'reply': 'wieġeb', 'points': '지점들', 'server': 'server_VALUE', 'data': 'data', 'prompt': 'prompt', 'enter': 'daħħal_851ea840', 'imported': '들여온파일', 'send': 'bagħat', 'main': 'serje', 'ROOT': 'pprojetta_għerq', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': 'tella_Fajls', 'pixels_file': 'pel_fajl', 'pixels_data': 'pel_data', 'edit': 'editja_VALUE', 'receive_until': '표시까지받기', 'selector': 'selettur', 'size': 'daqqas', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_GUI', 'y': '세로좌표', 'result': 'miżura', 'samples': '예제들', 'client': 'klijent', 'line': 'linja', 'report': 'validazzjoni_rapport', 'work': '작업경로', 'x': 'koordinat_x', 'python_checks': '파이썬검사', 'download': 'niżżel', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Proċess', 'content': 'Kontenut_VALUE', 'block': 'data_imblokka', 'marker': '확인표시', 'command': 'kmand', 'expected': '예상결과', 'shell': 'shell', 'drawing': 'tpinġija_mogħdija', 'f': 'fajl_entrata', 'transcript': '대화기록', 'offset': 'OFFSET_VALUE', 'path': 'mogħdija', 'screenshot': 'klipp_tal_iskrin', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_VALUE', 'cmd': '명령인수', 'name': 'isem', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
