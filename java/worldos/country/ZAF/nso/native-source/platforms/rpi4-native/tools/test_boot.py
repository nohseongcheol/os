#!/usr/bin/env python3
"""기존 Tsejana 호환 go_tsenya_tshedimošo_ntlha. kgonthe_data 구현: ../Ditholosi/부팅시험.py"""
import importlib as 가져오기
import sys as tshepedišotirišo_boleng
from pathlib import Path as Tsejana
tshepedišotirišo_boleng.path.insert(0, str(Tsejana(__file__).resolve().parents[1] / 'Ditholosi'))
if __name__ == '__main__':
    import runpy as tirišo_sethala_tirišo
    tirišo_sethala_tirišo.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('부팅시험')
    대응 = {'timeout': '시간제한', 'response': '응답자료', 'msg': 'Netweke_molaetša', 'exact': '정확한값', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'phethagatša_mošomo', 'cancel': 'Khansela_tiro', 'cmd_byte': 'taelo_paete', 'reply': 'fetola', 'points': '지점들', 'server': 'seba_boleng', 'data': 'data', 'prompt': 'temoši', 'enter': 'tsenya_851ea840', 'imported': '들여온파일', 'send': 'Romela', 'main': 'Diriša', 'ROOT': '기준', 'text': 'Sengwalwa', 'first_gui': '첫화면', 'pixel': 'phele', 'java_class': '자바클래스', 'upload': 'apolouto_Difaele', 'pixels_file': 'phele_faele', 'pixels_data': 'phele_data', 'edit': 'rulaganya_boleng', 'receive_until': '표시까지받기', 'selector': 'sekgethi', 'size': 'Bogolo', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': '둘째화면', 'y': '세로좌표', 'result': '결과', 'samples': '예제들', 'client': 'klaente', 'line': 'mothaladi', 'report': 'tiišetšo_pego', 'work': '작업경로', 'x': 'kamano_ya_x', 'python_checks': '파이썬검사', 'download': 'tanelouto', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': '마감시각', 'proc': 'tiragalo_a7054519', 'content': 'Diteng_boleng', 'block': 'data_thibela', 'marker': '확인표시', 'command': 'Taelo', 'expected': '예상결과', 'shell': 'šele', 'drawing': 'sethalwa_tsela', 'f': 'faele_go_tsenya_tshedimošo', 'transcript': '대화기록', 'offset': 'E_Šetšego_boleng', 'path': 'Tsejana', 'screenshot': 'pontšhosekerini', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': '출력결과', 'stream': 'Stream_boleng', 'cmd': '명령인수', 'name': 'Leina', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
