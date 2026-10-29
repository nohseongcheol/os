#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'ርእስ_እሴት', 'sources': '원문목록', 'i': '순번', 'info': 'የስርዓት_መረጃ', 'payload': 'የክፍያ_ጫና_ውሂብ', 'src': '원본주소', 'run': 'ፈጽም_ትእዛዝ', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'መደብ_ዱካ', 'dist': '배포경로', 'archive': 'ከዝን', 'output': '출력결과', 'root': 'ስር_አድራሻ', 'name': 'ስም', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
