#!/usr/bin/env python3
"""기존 መገዲ 호환 ምእታው_ነጥቢ. ትኽክለኛ_ሓበሬታ 구현: ../መሳርሒታት/실행파일시험.py"""
import importlib as 가져오기
import sys as ስርዓት_ስርሒት_ዋጋ
from pathlib import Path as መገዲ
ስርዓት_ስርሒት_ዋጋ.path.insert(0, str(መገዲ(__file__).resolve().parents[1] / 'መሳርሒታት'))
if __name__ == '__main__':
    import runpy as መተግበሪ_ተመዛዚ_መተግበሪ
    መተግበሪ_ተመዛዚ_መተግበሪ.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'መተግበሪ_ርእሲ_ሽፋን', 'offset': 'ሽፋን_ዋጋ', 'invalid': 'ዘይቅቡል_ሓበሬታ', 'path': 'መገዲ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'ቅረጽ_b87fd068', 'main': 'ኣኺድ', 'content': 'ትሕዝቶ_ዋጋ', 'source': '원본자료', 'name': 'ሽም', 'reference': '비교기준', 'ROOT': '기준', 'value': 'ዋጋ', 'report': 'ምርግጋፅ_ጸብጻብ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
