#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/예제빌드.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'ልኬት_ውሂብ', 'build_examples': '예제만들기', 'files': 'ፋይል_ዝርዝር', 'java': '자바실행', 'run': 'ፈጽም_ትእዛዝ', 'path': 'መተላለፊያ', 'p': 'ውሂብ_በቦታ_አስቀመጠ', 'readme': 'አንበኝ', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'ፍለጋ_መረጃ_ጠቆመ', 'classes': 'መደብ_ዱካ', 'repo': 'ማከማቻ_ዱካ', 'root': 'ስር_አድራሻ', 'content': 'ይዘት_እሴት', 'source': '원본자료', 'name': 'ስም', 'target': 'ዓላማ', 'manifest': '꾸러미명세', 'language': 'ቋንቋ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
