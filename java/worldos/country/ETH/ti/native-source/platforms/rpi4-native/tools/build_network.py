#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/ህነጽ_ማሕበራዊ_ኔትወርክ.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('ህነጽ_ማሕበራዊ_ኔትወርክ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ህነጽ_ማሕበራዊ_ኔትወርክ')
    대응 = {'obj': 'መዕለቢ_ፋይል', 'objects': 'መዓልቦ_ፋይላት', 'library': 'ቤት_ንባብ', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'ፋይል_ዝርዝር', 'source': '원본자료', 'run': 'ተግብር_ትእዛዝ', 'flags': '설정비트', 'path': 'መገዲ', 'build_network': 'ፍጠር_ማሕበራዊ_ኔትወርክ', 'cc': '시언어번역기', 'ar': 'ሰንድ_መሳርሒ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
