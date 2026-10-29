#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/셸시험.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'ኤክስ_አስተባባሪ', 'msg': 'መረብ_ኢሜይል', 'i': '순번', 'reply': 'መልስ', 'call': '호출', 'args': 'ነጋሪ_እሴት_ድርድር', 'chunk': '조각', 'data': 'ውሂብ', 'proc': 'ሂደቶች', 'long_text': '긴글', 'restored': '복원자료', 'send': 'ላክ', 'file': 'ፋይል', 'main': 'ማስኬጃ', 'found': 'ፈልግ_ልኬት', 'ROOT': 'አሳይ_ስር', 'text': 'ጽሁፍ', 'marker': '확인표시', 'command': 'ትእዛዝ', 'expected': '예상결과', 'pixel': 'ፒክስል', 'shell': 'ሼል', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'ጨርስ_ዝንፍ', 'image': 'ምስል', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'ልኬት', 'client': 'ተገልጋይ', 'line': 'መስመር', 'stream': 'ልቀቅ_እሴት', 'name': 'ስም', 'value': 'እሴት', 'receive': '수신하기', 'report': 'ማረጋገጥ_ዘገባ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
