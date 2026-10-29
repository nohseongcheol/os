#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/부팅시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': 'erantzun_1262b476', 'msg': 'sare_mezu', 'exact': 'BERDIN_balio', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Exekutatu', 'cancel': 'Utzi_kirurgia', 'cmd_byte': 'komando_byte', 'reply': 'erantzun', 'points': '지점들', 'server': 'zerbitzari_balio', 'data': 'datuak', 'prompt': 'eskatu', 'enter': 'sartu', 'imported': '들여온파일', 'send': 'bidali', 'main': 'Exekutatu_2', 'ROOT': 'Project_erro', 'text': 'Testua', 'first_gui': '첫화면', 'pixel': 'pixel', 'java_class': '자바클래스', 'upload': 'Upload_Fitxategiak', 'pixels_file': 'pixel_fitxategi', 'pixels_data': 'pixel_datuak', 'edit': 'edizio_balio', 'receive_until': '표시까지받기', 'selector': '준비선택기', 'size': 'Tamaina', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SEGUNDOA_GUI', 'y': 'Y_koordenatu', 'result': 'EMAITZA', 'samples': '예제들', 'client': 'bezero', 'line': 'Marra', 'report': 'balidazio_txosten', 'work': '작업경로', 'x': 'X_koordenatu', 'python_checks': '파이썬검사', 'download': 'deskarga', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Prozesua', 'content': 'eduki_balio', 'block': 'datuak_blokeatu', 'marker': '확인표시', 'command': 'Komandoa', 'expected': '예상결과', 'shell': 'shell', 'drawing': '그림경로', 'f': 'fitxategi_sarrera', 'transcript': '대화기록', 'offset': 'Geruzak_balio', 'path': 'Bide_izena', 'screenshot': 'pantaila_mozketa', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_balio', 'cmd': '명령인수', 'name': 'Izena', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
