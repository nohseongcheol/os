#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/부팅시험.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Mtandao_ujumbe', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'tekeleza_kazi', 'cancel': 'ghairi_upasuaji', 'cmd_byte': 'amri_baiti', 'reply': 'jibu', 'points': '지점들', 'server': 'seva_thamani', 'data': 'data', 'prompt': 'kisituo', 'enter': 'ingiza', 'imported': '들여온파일', 'send': 'tuma', 'main': 'endesha', 'ROOT': '기준', 'text': 'SMS', 'first_gui': '첫화면', 'pixel': 'elepi', 'java_class': '자바클래스', 'upload': 'pakia_Faili', 'pixels_file': 'elepi_faili', 'pixels_data': 'elepi_data', 'edit': 'hariri_thamani', 'receive_until': '표시까지받기', 'selector': 'kiteuzi', 'size': 'panga_ukubwa', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': 'Kitufe_cha_Y_kiratibu', 'result': '결과', 'samples': '예제들', 'client': 'teja', 'line': 'laini', 'report': 'uhakikishi_ripoti', 'work': '작업경로', 'x': 'jira_x', 'python_checks': '파이썬검사', 'download': 'pakua', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'Mchakato', 'content': 'maudhui_thamani', 'block': 'data_zuia', 'marker': '확인표시', 'command': 'amri', 'expected': '예상결과', 'shell': 'sheli', 'drawing': 'mchoro_njia', 'f': 'faili_ingizo', 'transcript': '대화기록', 'offset': 'Chipua_thamani', 'path': 'njia', 'screenshot': 'picha_ya_skrini', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_thamani', 'cmd': '명령인수', 'name': 'Jina', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
