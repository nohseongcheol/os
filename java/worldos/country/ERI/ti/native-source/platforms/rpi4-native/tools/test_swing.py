#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/화면요소시험.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': '가로좌표', 's': 'ሕብረ_ቁምፊ_ሓበሬታ', 'i': '순번', 'sel': 'መራፂ_a916db4e', 'seconds': '초단위', 'log': 'ምዝጉብ_ሪጋ', 'data': 'ሓበሬታ', 'at': '현재위치', 'send': 'ለኣኽ', 'main': 'ኣኺድ', 'req': '요청값', 'hot': 'ኣቋራጭ_ዋጋ', 'pump': 'መትሓዚ_ፍጻመ', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'ትእዛዝ', 'shell': 'ሽፋን', 'f': 'ፋይል_ምእታው', 'click': 'ጠዉቕ_መጠወቒ', 'k': '셋째순번', 'c': 'ኮድ_ፊደል', 'r': '반환값', 'p': '자료위치', 'command_mode': 'ትእዛዝ_ኹነት', 'end': 'ኣቑም_ሽፋን', 'classes': 'ክፍሊ_መገዲ', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'ምርግጋፅ_ጸብጻብ', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
