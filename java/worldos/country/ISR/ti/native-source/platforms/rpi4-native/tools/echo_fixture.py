#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ሓበሬታ', 'e': '보조항목', 'connection': 'ርክብ_e05f319b', 'f': 'ፋይል_ምእታው', 'peer': 'መዘና_ዋጋ', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'ርክብ_ቁጽጽር', 'EchoFixture': '되돌림시험서버', 'args': 'ሓባሪ_ቁጽሪ_ተርታ', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
