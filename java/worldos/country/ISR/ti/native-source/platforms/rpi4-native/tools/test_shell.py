#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/셸시험.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': '가로좌표', 'msg': 'ማሕበራዊ_ኔትወርክ_መልእኽቲ', 'i': '순번', 'reply': 'መልስ', 'call': '호출', 'args': 'ሓባሪ_ቁጽሪ_ተርታ', 'chunk': '조각', 'data': 'ሓበሬታ', 'proc': 'መስርሕ', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ለኣኽ', 'file': 'ፋይል', 'main': 'ኣኺድ', 'found': '찾은결과', 'ROOT': '기준', 'text': 'ጽሑፍ', 'marker': '확인표시', 'command': 'ትእዛዝ', 'expected': '예상결과', 'pixel': 'ንጣብ', 'shell': 'ሽፋን', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ኣቑም_ሽፋን', 'image': 'ምስሊ', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'ዓሚል', 'line': 'መስመር', 'stream': 'ወሓዚ_ዋጋ', 'name': 'ሽም', 'value': 'ዋጋ', 'receive': '수신하기', 'report': 'ምርግጋፅ_ጸብጻብ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
