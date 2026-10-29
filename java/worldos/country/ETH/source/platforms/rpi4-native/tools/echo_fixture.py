#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ውሂብ', 'e': '보조항목', 'connection': 'ግንኙነት_e05f319b', 'f': 'ፋይል_ምዝግብ', 'peer': 'አቻ_እሴት', 'self': '자신', 'udp': '전문제어', 't': 'ተርሚናል_ምዝግብ', 'tcp': 'ግንኙነት_ቁጥጥር', 'EchoFixture': '되돌림시험서버', 'args': 'ነጋሪ_እሴት_ድርድር', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
