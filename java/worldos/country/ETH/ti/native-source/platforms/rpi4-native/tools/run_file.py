#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/ተግብር_ፋይል.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('ተግብር_ፋይል', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ተግብር_ፋይል')
    대응 = {'timeout': '시간제한', 's': 'ሕብረ_ቁምፊ_ሓበሬታ', 'i': '순번', 'match': '일치', 'files': 'ፋይል_ዝርዝር', 'program': 'መተግበሪ', 'executable': '실행가능파일', 'args': 'ሓባሪ_ቁጽሪ_ተርታ', 'chunk': '조각', 'data': 'ሓበሬታ', 'proc': 'መስርሕ', 'send': 'ለኣኽ', 'main': 'ኣኺድ', 'marker': '확인표시', 'command': 'ትእዛዝ', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'ተግብር_ትእዛዝ', 'p': '자료위치', 'parser': '인수해석기', 'options': 'ኣማራጽታት', 'kind': 'መደብ_ዋጋ', 'selector': 'መራፂ', 'upload_data': 'ስቐል_ሓበሬታ', 'end': 'ኣቑም_ሽፋን', 'n': '개수', 'd': 'መዓልቦ_ሓበሬታ', 'key': '누름값', 'output': '출력결과', 'line': 'መስመር', 'name': 'ሽም', 'upload_name': 'ስቐል_ሽም', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
