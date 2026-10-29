#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/ተግብር_ትእዛዝ.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('ተግብር_ትእዛዝ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ተግብር_ትእዛዝ')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'ኣኺድ_ዴስክቶፕ', 'main': 'ኣኺድ', 'host': 'አዐንግድ', 'status': 'ደረጃ_ዋጋ', 'NetworkBridge': '통신다리', 'ROOT': '기준', 'bridge': '연결다리', 'loader': '적재기', 'base': 'ድሕረባይታ_ዋጋ', 'options': 'ኣማራጽታት', 'binary': 'ጽምዳዊ', 'args': 'ሓባሪ_ቁጽሪ_ተርታ', 'command': 'ትእዛዝ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
