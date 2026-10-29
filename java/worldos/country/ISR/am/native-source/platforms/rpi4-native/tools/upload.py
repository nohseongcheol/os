#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/መጫን_ፋይሎች.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('መጫን_ፋይሎች', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('መጫን_ፋይሎች')
    대응 = {'data': 'ውሂብ', 'i': '순번', 'name': 'ስም', 'c': 'የቁምፊ_ኮድ', 'p': 'ውሂብ_በቦታ_አስቀመጠ', 'args': 'ነጋሪ_እሴት_ድርድር'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
