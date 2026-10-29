#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/바탕화면시험.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'jira_x', 'typing': '글자입력', 'message': '알림문', 'start': 'endesha', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'ishara', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Mchakato', 'data': 'data', 'main': 'endesha', 'w': '너비값', 'init': '초기값', 'block': 'data_zuia', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'report': 'uhakikishi_ripoti', 'until': '까지', 'clipboard': 'ubao_nakili_thamani', 'dst': 'fikio_anwani', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'namba_ya_kituo', 'offset': 'Chipua_thamani', 'h': '높이값', 'src': '원본주소', 'event': 'tukio', 'encoding': 'seti_kibambo', 'size': 'panga_ukubwa', 'key': '누름값', 'pixels': '화소들', 'y': 'Kitufe_cha_Y_kiratibu', 'output': '출력결과', 'symbol': 'ishara_thamani', 'client': 'teja', 'char': 'kibambo_data', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
