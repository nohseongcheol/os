#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/창시험.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'ኤክስ_አስተባባሪ', 's': 'ኅብረቁምፊ_ውሂብ', 'xy': 'መዋያ_ጥምድ', 'sel': 'መራጭ_a916db4e', 'seconds': '초단위', 'log': 'መዝግብ_ረድፍ', 'at': '현재위치', 'send': 'ላክ', 'main': 'ማስኬጃ', 'req': '요청값', 'hot': 'አቋራጭ_እሴት', 'pump': 'እጀታ_ፍጻሜ', 'ROOT': 'አሳይ_ስር', 'marker': '확인표시', 'b': '둘째값', 'command': 'ትእዛዝ', 'shell': 'ሼል', 'f': 'ፋይል_ምዝግብ', 'color': '색상', 'click': 'ጠቅ_አድርግ_አዝራር', 'k': '셋째순번', 'c': 'የቁምፊ_ኮድ', 'r': '반환값', 'p': 'ውሂብ_በቦታ_አስቀመጠ', 'done': '완료량', 'end': 'ጨርስ_ዝንፍ', 'command_mode': 'ትእዛዝ_ሁነታ', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'ልኬት', 'report': 'ማረጋገጥ_ዘገባ', 'dest': 'መድረሻ_እሴት_በቦታ_አስቀመጠ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
