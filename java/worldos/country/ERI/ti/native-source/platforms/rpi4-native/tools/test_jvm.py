#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'ሕብረ_ቁምፊ_ሓበሬታ', 'actual': '실제결과', 'match': '일치', 'payload': 'ጽዕነት_ክፍሊት_ሓበሬታ', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'ኣኺድ', 'ROOT': '기준', 'text': 'ጽሑፍ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'ክፍሊ_መገዲ', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'ሽም', 'jar': '자바꾸러미', 'report': 'ምርግጋፅ_ጸብጻብ', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
