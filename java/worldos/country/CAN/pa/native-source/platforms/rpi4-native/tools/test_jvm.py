#!/usr/bin/env python3
"""기존 ਮਾਰਗ 호환 ਦਾਖਲਾ_ਪੌਇੰਟ. ਅਸਲ_ਸਮੱਗਰੀ 구현: ../ਸਾਧਨ/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ
from pathlib import Path as ਮਾਰਗ
ਸਿਸਟਮ_ਚਲਾਉਣਾ_ਕੀਮਤ.path.insert(0, str(ਮਾਰਗ(__file__).resolve().parents[1] / 'ਸਾਧਨ'))
if __name__ == '__main__':
    import runpy as ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ
    ਐਪਲੀਕੇਸ਼_ਐਪ_ਡ੍ਰਾਅਰ.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ', 'actual': 'ਅਸਲ_ਮਾਪ', 'match': '일치', 'payload': 'ਪੇਲੋਡ_ਸਮੱਗਰੀ', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'ਚਲਾਓ_2', 'ROOT': 'ਪ੍ਰੋਜੈਕਟ_ਰੂਟ', 'text': 'ਟੈਕਸਟ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'ਸ੍ਰੇਣੀ_ਰਸਤਾ', 'output': '출력결과', 'result': 'ਮਾਪ', 'cmd': '명령인수', 'name': 'ਨਾਂ', 'jar': '자바꾸러미', 'report': 'ਮਾਨਤਾ_ਵਿਵਰਨ', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
