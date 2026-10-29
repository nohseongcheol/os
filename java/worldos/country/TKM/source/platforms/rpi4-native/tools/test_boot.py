#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/부팅시험.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Tor_habar', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'ýerine_ýetir_tabşyryk', 'cancel': 'bes_et_amal', 'cmd_byte': 'buýruk_baýt', 'reply': 'jogap_bermek', 'points': '지점들', 'server': 'serwer_baha', 'data': 'maglumat', 'prompt': 'çagyryş', 'enter': 'giriz_851ea840', 'imported': '들여온파일', 'send': 'iber', 'main': 'Bitir', 'ROOT': '기준', 'text': 'Metin', 'first_gui': '첫화면', 'pixel': 'pel', 'java_class': '자바클래스', 'upload': 'ýükle_Faýllar', 'pixels_file': 'pel_faýl', 'pixels_data': 'pel_maglumat', 'edit': 'redaktirle_baha', 'receive_until': '표시까지받기', 'selector': 'saýlaýjy', 'size': 'Ululyk', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'müşderi', 'line': 'setir', 'report': 'barlag_hasabat', 'work': '작업경로', 'x': 'x_koordinatasy', 'python_checks': '파이썬검사', 'download': 'göçürim', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Proses', 'content': 'Mazmun_baha', 'block': 'maglumat_bökde', 'marker': '확인표시', 'command': 'buýruk', 'expected': '예상결과', 'shell': 'gabyjak', 'drawing': 'çyzgy_ýol', 'f': 'faýl_girizmeklik', 'transcript': '대화기록', 'offset': 'Süýşüriş_baha', 'path': 'Ýol', 'screenshot': 'ekran_gyrkma', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_baha', 'cmd': '명령인수', 'name': 'Ad', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
