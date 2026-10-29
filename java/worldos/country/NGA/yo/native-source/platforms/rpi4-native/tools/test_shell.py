#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/셸시험.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'ibi_ìtọ́kasí_x', 'msg': 'Alásopọ̀_iṣé', 'i': '순번', 'reply': 'Fèsì', 'call': '호출', 'args': 'ágúmẹ́ntì_ÀRÉÈ', 'chunk': '조각', 'data': 'détà', 'proc': 'Ìlànà', 'long_text': '긴글', 'restored': '복원자료', 'send': 'í_meèlì', 'file': 'Fáìlì', 'main': 'Rọ́ọ̀nù', 'found': '찾은결과', 'ROOT': '기준', 'text': 'SMS', 'marker': '확인표시', 'command': 'Àṣẹ', 'expected': '예상결과', 'pixel': 'píkísẹ̀', 'shell': 'ṣẹ́ẹ̀lì', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'parí_Ìtayọ', 'image': 'àwòrán', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'aṣojú', 'line': 'ìlà', 'stream': 'Stream_iye', 'name': 'Orúkọ', 'value': 'iye', 'receive': '수신하기', 'report': 'Àfọwọ́sí_ìjábọ̀', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
