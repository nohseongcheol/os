#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/실행파일시험.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'ልኬት_ውሂብ', 'expected': '예상결과', 'phoff': 'ፕሮግራም_ርእስ_ዝንፍ', 'offset': 'ዝንፍ_እሴት', 'invalid': 'ልክ_ያልኾነ_ውሂብ', 'path': 'መተላለፊያ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'ልኬት', 'format_': 'ቅርጸት_b87fd068', 'main': 'ማስኬጃ', 'content': 'ይዘት_እሴት', 'source': '원본자료', 'name': 'ስም', 'reference': 'ንጽጽር_መነሻ', 'ROOT': 'አሳይ_ስር', 'value': 'እሴት', 'report': 'ማረጋገጥ_ዘገባ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
