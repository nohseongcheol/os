#!/usr/bin/env python3
"""기존 መተላለፊያ 호환 ምዝግብ_ቦታ. ትክክለኛ_ውሂብ 구현: ../መሳሪያዎች/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ስርዓተ_ክወና_እሴት
from pathlib import Path as መተላለፊያ
ስርዓተ_ክወና_እሴት.path.insert(0, str(መተላለፊያ(__file__).resolve().parents[1] / 'መሳሪያዎች'))
if __name__ == '__main__':
    import runpy as ፕሮግራም_የመተግበሪያ_መሳቢያ
    ፕሮግራም_የመተግበሪያ_መሳቢያ.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'ኅብረቁምፊ_ውሂብ', 'actual': 'ትክክለኛ_ልኬት', 'match': '일치', 'payload': 'የክፍያ_ጫና_ውሂብ', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'ማስኬጃ', 'ROOT': 'አሳይ_ስር', 'text': 'ጽሁፍ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'መደብ_ዱካ', 'output': '출력결과', 'result': 'ልኬት', 'cmd': '명령인수', 'name': 'ስም', 'jar': '자바꾸러미', 'report': 'ማረጋገጥ_ዘገባ', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
