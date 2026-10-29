#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/바탕화면시험.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'ibi_ìtọ́kasí_x', 'typing': '글자입력', 'message': '알림문', 'start': 'Rọ́ọ̀nù', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'àmì', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Ìlànà', 'data': 'détà', 'main': 'Rọ́ọ̀nù', 'w': '너비값', 'init': '초기값', 'block': 'détà_sèdíwọ', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'report': 'Àfọwọ́sí_ìjábọ̀', 'until': '까지', 'clipboard': 'aka_ọlọ́pọ́n_iye', 'dst': 'èbúté_àdírẹ́ẹ̀sì', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'Ìtayọ_iye', 'h': '높이값', 'src': '원본주소', 'event': 'ìgbéṣẹ̀', 'encoding': 'àkójọpọ̀_ẹyọ_ọ̀rọ̀', 'size': 'Ìwọ̀n', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'àmì_iye', 'client': 'aṣojú', 'char': 'ẹyọ_ọ̀rọ̀_détà', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
