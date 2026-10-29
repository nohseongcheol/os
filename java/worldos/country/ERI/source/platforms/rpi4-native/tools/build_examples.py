#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/예제빌드.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'ፋይል_ዝርዝር', 'java': '자바실행', 'run': 'ተግብር_ትእዛዝ', 'path': 'መገዲ', 'p': '자료위치', 'readme': 'ኣንብበኒ', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': '색인', 'classes': 'ክፍሊ_መገዲ', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'ትሕዝቶ_ዋጋ', 'source': '원본자료', 'name': 'ሽም', 'target': 'ዕላማ', 'manifest': '꾸러미명세', 'language': 'ቋንቋ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
