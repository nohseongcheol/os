#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/ስቐል_ፋይላት.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('ስቐል_ፋይላት', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ስቐል_ፋይላት')
    대응 = {'data': 'ሓበሬታ', 'i': '순번', 'name': 'ሽም', 'c': 'ኮድ_ፊደል', 'p': '자료위치', 'args': 'ሓባሪ_ቁጽሪ_ተርታ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
