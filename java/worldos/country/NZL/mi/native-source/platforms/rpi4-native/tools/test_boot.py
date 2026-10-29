#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/부팅시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'whatunga_karere', 'exact': 'EXACT_uara', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'kawe_tūmahi', 'cancel': 'whakakore_mahi', 'cmd_byte': 'tono_paita', 'reply': 'whakautu', 'points': '지점들', 'server': 'tūmau_uara', 'data': 'raraunga', 'prompt': 'tohuaki', 'enter': 'tāuru', 'imported': '들여온파일', 'send': 'tuku', 'main': 'whakahaere', 'ROOT': 'whakaatu_pūtake', 'text': 'Ngā_kupu', 'first_gui': '첫화면', 'pixel': 'pika', 'java_class': '자바클래스', 'upload': 'tukuatu_Ngā_Kōnae', 'pixels_file': 'pika_kōnae', 'pixels_data': 'pika_raraunga', 'edit': 'whakatika_uara', 'receive_until': '표시까지받기', 'selector': 'pūtīpako', 'size': 'rahi', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SECOND_AKW', 'y': '세로좌표', 'result': 'mēhua', 'samples': '예제들', 'client': 'kiritaki', 'line': 'hononga', 'report': 'whakamana_pūrongo', 'work': '작업경로', 'x': 'taunga_x', 'python_checks': '파이썬검사', 'download': 'tikiake', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Hātepe', 'content': 'Ihirangi_uara', 'block': 'raraunga_aukati', 'marker': '확인표시', 'command': 'tono', 'expected': '예상결과', 'shell': 'anga', 'drawing': 'tātuhi_ara', 'f': 'kōnae_tāurunga', 'transcript': '대화기록', 'offset': 'OFFSET_uara', 'path': 'ara', 'screenshot': 'topenga_mata', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'roma_uara', 'cmd': '명령인수', 'name': 'Ingoa', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
